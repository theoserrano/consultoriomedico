"""
Classe de conexão e gerenciamento do Firebase Firestore
Sistema de Consultório Médico - NoSQL Integration
"""

import logging
from typing import Optional, Dict, List, Any
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from nosql.config_nosql import FirebaseConfig

# Configurar logging
logger = logging.getLogger("consultorio.firebase")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO if not FirebaseConfig.DEBUG else logging.DEBUG)


class FirebaseDatabase:
    """
    Classe para gerenciar conexão e operações com Firebase Firestore.
    Não interfere com o banco MySQL existente.
    """
    
    _instance: Optional['FirebaseDatabase'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern para garantir uma única instância"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa a conexão com Firebase (apenas uma vez)"""
        if not FirebaseDatabase._initialized:
            self.db: Optional[firestore.client] = None
            self.collections = {
                'pacientes': FirebaseConfig.COLLECTION_PACIENTES,
                'medicos': FirebaseConfig.COLLECTION_MEDICOS,
                'clinicas': FirebaseConfig.COLLECTION_CLINICAS,
                'consultas': FirebaseConfig.COLLECTION_CONSULTAS,
            }
            FirebaseDatabase._initialized = True
    
    def connect(self) -> bool:
        """
        Conecta ao Firebase Firestore.
        
        Returns:
            bool: True se conectado com sucesso, False caso contrário
        """
        if self.db is not None:
            logger.info("Firestore já está conectado")
            return True
        
        try:
            # Validar configuração
            valid, message = FirebaseConfig.validate()
            if not valid:
                logger.error(f"Configuração inválida: {message}")
                return False
            
            # Inicializar Firebase Admin SDK
            if not firebase_admin._apps:
                cred = credentials.Certificate(FirebaseConfig.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK inicializado")
            
            # Obter cliente Firestore
            self.db = firestore.client()
            project_id = self.db.project
            logger.info(f"Conectado ao Firestore - Projeto: {project_id}")
            logger.info(f"Modo de modelagem: {FirebaseConfig.MODELING_MODE}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"Arquivo de credenciais não encontrado: {FirebaseConfig.FIREBASE_CREDENTIALS_PATH}")
            logger.error("Baixe o arquivo JSON de credenciais do Firebase Console")
            return False
        except Exception as e:
            logger.error(f"Erro ao conectar ao Firestore: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao Firestore"""
        return self.db is not None
    
    def get_collection(self, collection_name: str):
        """
        Obtém referência para uma coleção.
        
        Args:
            collection_name: Nome da coleção ('pacientes', 'medicos', 'clinicas', 'consultas')
        
        Returns:
            CollectionReference: Referência para a coleção
        """
        if not self.is_connected():
            raise ConnectionError("Não conectado ao Firestore. Execute connect() primeiro.")
        
        collection = self.collections.get(collection_name, collection_name)
        return self.db.collection(collection)
    
    # ==================== OPERAÇÕES CREATE ====================
    
    def create_document(self, collection_name: str, document_id: str, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Cria um novo documento em uma coleção.
        
        Args:
            collection_name: Nome da coleção
            document_id: ID do documento
            data: Dados do documento
        
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            collection = self.get_collection(collection_name)
            collection.document(document_id).set(data)
            logger.info(f"Documento criado: {collection_name}/{document_id}")
            return True, f"Documento criado com sucesso: {document_id}"
        except Exception as e:
            logger.error(f"Erro ao criar documento: {e}")
            return False, str(e)
    
    def create_document_auto_id(self, collection_name: str, data: Dict[str, Any]) -> tuple[bool, str, Optional[str]]:
        """
        Cria um novo documento com ID automático.
        
        Args:
            collection_name: Nome da coleção
            data: Dados do documento
        
        Returns:
            tuple[bool, str, str]: (sucesso, mensagem, document_id)
        """
        try:
            collection = self.get_collection(collection_name)
            doc_ref = collection.add(data)
            doc_id = doc_ref[1].id
            logger.info(f"Documento criado com ID automático: {collection_name}/{doc_id}")
            return True, f"Documento criado com sucesso", doc_id
        except Exception as e:
            logger.error(f"Erro ao criar documento: {e}")
            return False, str(e), None
    
    # ==================== OPERAÇÕES READ ====================
    
    def get_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um documento por ID.
        
        Args:
            collection_name: Nome da coleção
            document_id: ID do documento
        
        Returns:
            Dict ou None: Dados do documento ou None se não encontrado
        """
        try:
            doc = self.get_collection(collection_name).document(document_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['_id'] = doc.id  # Adicionar ID ao documento
                return data
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar documento: {e}")
            return None
    
    def get_all_documents(self, collection_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca todos os documentos de uma coleção.
        
        Args:
            collection_name: Nome da coleção
            limit: Limite de documentos (opcional)
        
        Returns:
            List[Dict]: Lista de documentos
        """
        try:
            query = self.get_collection(collection_name)
            if limit:
                query = query.limit(limit)
            
            docs = query.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['_id'] = doc.id
                results.append(data)
            
            logger.debug(f"Buscados {len(results)} documentos de {collection_name}")
            return results
        except Exception as e:
            logger.error(f"Erro ao buscar documentos: {e}")
            return []
    
    def query_documents(self, collection_name: str, filters: List[tuple], 
                        order_by: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca documentos com filtros.
        
        Args:
            collection_name: Nome da coleção
            filters: Lista de tuplas (campo, operador, valor)
                     Exemplo: [('especialidade', '==', 'Cardiologia')]
            order_by: Campo para ordenação (opcional)
            limit: Limite de documentos (opcional)
        
        Returns:
            List[Dict]: Lista de documentos que atendem aos filtros
        """
        try:
            query = self.get_collection(collection_name)
            
            # Aplicar filtros
            for field, operator, value in filters:
                query = query.where(filter=FieldFilter(field, operator, value))
            
            # Aplicar ordenação
            if order_by:
                query = query.order_by(order_by)
            
            # Aplicar limite
            if limit:
                query = query.limit(limit)
            
            docs = query.stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                data['_id'] = doc.id
                results.append(data)
            
            logger.debug(f"Query retornou {len(results)} documentos")
            return results
        except Exception as e:
            logger.error(f"Erro ao fazer query: {e}")
            return []
    
    # ==================== OPERAÇÕES UPDATE ====================
    
    def update_document(self, collection_name: str, document_id: str, 
                       data: Dict[str, Any], merge: bool = True) -> tuple[bool, str]:
        """
        Atualiza um documento.
        
        Args:
            collection_name: Nome da coleção
            document_id: ID do documento
            data: Dados a atualizar
            merge: Se True, faz merge com dados existentes. Se False, substitui.
        
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            doc_ref = self.get_collection(collection_name).document(document_id)
            if merge:
                doc_ref.update(data)
            else:
                doc_ref.set(data)
            logger.info(f"Documento atualizado: {collection_name}/{document_id}")
            return True, "Documento atualizado com sucesso"
        except Exception as e:
            logger.error(f"Erro ao atualizar documento: {e}")
            return False, str(e)
    
    # ==================== OPERAÇÕES DELETE ====================
    
    def delete_document(self, collection_name: str, document_id: str) -> tuple[bool, str]:
        """
        Deleta um documento.
        
        Args:
            collection_name: Nome da coleção
            document_id: ID do documento
        
        Returns:
            tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            self.get_collection(collection_name).document(document_id).delete()
            logger.info(f"Documento deletado: {collection_name}/{document_id}")
            return True, "Documento deletado com sucesso"
        except Exception as e:
            logger.error(f"Erro ao deletar documento: {e}")
            return False, str(e)
    
    def delete_documents_by_query(self, collection_name: str, filters: List[tuple]) -> tuple[bool, str, int]:
        """
        Deleta documentos que atendem aos filtros.
        
        Args:
            collection_name: Nome da coleção
            filters: Lista de tuplas (campo, operador, valor)
        
        Returns:
            tuple[bool, str, int]: (sucesso, mensagem, quantidade deletada)
        """
        try:
            docs = self.query_documents(collection_name, filters)
            count = 0
            for doc in docs:
                self.delete_document(collection_name, doc['_id'])
                count += 1
            
            logger.info(f"{count} documentos deletados de {collection_name}")
            return True, f"{count} documentos deletados", count
        except Exception as e:
            logger.error(f"Erro ao deletar documentos: {e}")
            return False, str(e), 0
    
    # ==================== UTILIDADES ====================
    
    def collection_exists(self, collection_name: str) -> bool:
        """Verifica se uma coleção existe (tem documentos)"""
        try:
            docs = self.get_collection(collection_name).limit(1).stream()
            return len(list(docs)) > 0
        except Exception:
            return False
    
    def count_documents(self, collection_name: str) -> int:
        """Conta o número de documentos em uma coleção"""
        try:
            docs = self.get_collection(collection_name).stream()
            return len(list(docs))
        except Exception as e:
            logger.error(f"Erro ao contar documentos: {e}")
            return 0
    
    def close(self):
        """Fecha a conexão (Firebase Admin SDK não precisa de close explícito)"""
        logger.info("Conexão Firestore encerrada")
        self.db = None


# Instância global (singleton)
firebase_db = FirebaseDatabase()

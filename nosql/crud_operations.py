"""
Operações CRUD para Firebase Firestore
Sistema de Consultório Médico - NoSQL Integration
"""

from typing import Dict, Any, List, Optional, Tuple
from nosql.db_nosql import firebase_db
from nosql.models_nosql import FirestoreModels, FirestoreQueries
from nosql.config_nosql import FirebaseConfig
import logging

logger = logging.getLogger("consultorio.firebase.crud")


class FirestoreCRUD:
    """Operações CRUD de alto nível para o Firestore"""
    
    def __init__(self):
        self.db = firebase_db
    
    # ==================== PACIENTES ====================
    
    def criar_paciente(self, cpf: str, nome: str, data_nascimento: str,
                      genero: str, telefone: str, email: str) -> Tuple[bool, str]:
        """
        Cria um novo paciente no Firestore.
        
        Args:
            cpf: CPF do paciente (usado como ID do documento)
            nome: Nome completo
            data_nascimento: Data de nascimento (YYYY-MM-DD)
            genero: M ou F
            telefone: Telefone
            email: Email
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            doc_data = FirestoreModels.paciente_to_firestore(
                cpf, nome, data_nascimento, genero, telefone, email
            )
            return self.db.create_document('pacientes', cpf, doc_data)
        except Exception as e:
            logger.error(f"Erro ao criar paciente: {e}")
            return False, str(e)
    
    def buscar_paciente(self, cpf: str) -> Optional[Dict[str, Any]]:
        """
        Busca um paciente por CPF.
        
        Args:
            cpf: CPF do paciente
        
        Returns:
            Dict ou None: Dados do paciente ou None se não encontrado
        """
        return self.db.get_document('pacientes', cpf)
    
    def listar_pacientes(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Lista todos os pacientes.
        
        Args:
            limit: Limite de resultados (opcional)
        
        Returns:
            List[Dict]: Lista de pacientes
        """
        return self.db.get_all_documents('pacientes', limit)
    
    def atualizar_paciente(self, cpf: str, dados: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Atualiza dados de um paciente.
        
        Args:
            cpf: CPF do paciente
            dados: Dados a atualizar (apenas os campos que mudaram)
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        from datetime import datetime
        dados['updated_at'] = datetime.now()
        return self.db.update_document('pacientes', cpf, dados, merge=True)
    
    def deletar_paciente(self, cpf: str) -> Tuple[bool, str]:
        """
        Deleta um paciente.
        
        Args:
            cpf: CPF do paciente
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        return self.db.delete_document('pacientes', cpf)
    
    # ==================== MÉDICOS ====================
    
    def criar_medico(self, codigo: str, nome: str, genero: str,
                    telefone: str, email: str, especialidade: str) -> Tuple[bool, str]:
        """
        Cria um novo médico no Firestore.
        
        Args:
            codigo: Código do médico (usado como ID do documento)
            nome: Nome completo
            genero: M ou F
            telefone: Telefone
            email: Email
            especialidade: Especialidade médica
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            doc_data = FirestoreModels.medico_to_firestore(
                codigo, nome, genero, telefone, email, especialidade
            )
            return self.db.create_document('medicos', codigo, doc_data)
        except Exception as e:
            logger.error(f"Erro ao criar médico: {e}")
            return False, str(e)
    
    def buscar_medico(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Busca um médico por código"""
        return self.db.get_document('medicos', codigo)
    
    def listar_medicos(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista todos os médicos"""
        return self.db.get_all_documents('medicos', limit)
    
    def buscar_medicos_por_especialidade(self, especialidade: str) -> List[Dict[str, Any]]:
        """
        Busca médicos por especialidade.
        
        Args:
            especialidade: Nome da especialidade
        
        Returns:
            List[Dict]: Lista de médicos da especialidade
        """
        filters = FirestoreQueries.medicos_por_especialidade(especialidade)
        return self.db.query_documents('medicos', filters)
    
    def atualizar_medico(self, codigo: str, dados: Dict[str, Any]) -> Tuple[bool, str]:
        """Atualiza dados de um médico"""
        from datetime import datetime
        dados['updated_at'] = datetime.now()
        return self.db.update_document('medicos', codigo, dados, merge=True)
    
    def deletar_medico(self, codigo: str) -> Tuple[bool, str]:
        """Deleta um médico"""
        return self.db.delete_document('medicos', codigo)
    
    # ==================== CLÍNICAS ====================
    
    def criar_clinica(self, codigo: str, nome: str, endereco: str,
                     telefone: str, email: str) -> Tuple[bool, str]:
        """
        Cria uma nova clínica no Firestore.
        
        Args:
            codigo: Código da clínica (usado como ID do documento)
            nome: Nome da clínica
            endereco: Endereço completo
            telefone: Telefone
            email: Email
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        try:
            doc_data = FirestoreModels.clinica_to_firestore(
                codigo, nome, endereco, telefone, email
            )
            return self.db.create_document('clinicas', codigo, doc_data)
        except Exception as e:
            logger.error(f"Erro ao criar clínica: {e}")
            return False, str(e)
    
    def buscar_clinica(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Busca uma clínica por código"""
        return self.db.get_document('clinicas', codigo)
    
    def listar_clinicas(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista todas as clínicas"""
        return self.db.get_all_documents('clinicas', limit)
    
    def atualizar_clinica(self, codigo: str, dados: Dict[str, Any]) -> Tuple[bool, str]:
        """Atualiza dados de uma clínica"""
        from datetime import datetime
        dados['updated_at'] = datetime.now()
        return self.db.update_document('clinicas', codigo, dados, merge=True)
    
    def deletar_clinica(self, codigo: str) -> Tuple[bool, str]:
        """Deleta uma clínica"""
        return self.db.delete_document('clinicas', codigo)
    
    # ==================== CONSULTAS ====================
    
    def criar_consulta(self, cpf_paciente: str, cod_medico: str, cod_clinica: str,
                      data_hora: str, observacoes: str = "", status: str = "agendada") -> Tuple[bool, str, Optional[str]]:
        """
        Cria uma nova consulta no Firestore.
        O formato depende do modo configurado (embedded ou referenced).
        
        Args:
            cpf_paciente: CPF do paciente
            cod_medico: Código do médico
            cod_clinica: Código da clínica
            data_hora: Data e hora da consulta
            observacoes: Observações da consulta
            status: Status (agendada, realizada, cancelada)
        
        Returns:
            Tuple[bool, str, str]: (sucesso, mensagem, document_id)
        """
        try:
            # Se modo embedded, buscar dados completos
            if FirebaseConfig.MODELING_MODE == 'embedded':
                paciente_data = self.buscar_paciente(cpf_paciente)
                medico_data = self.buscar_medico(cod_medico)
                clinica_data = self.buscar_clinica(cod_clinica)
                
                if not paciente_data:
                    return False, f"Paciente {cpf_paciente} não encontrado", None
                if not medico_data:
                    return False, f"Médico {cod_medico} não encontrado", None
                if not clinica_data:
                    return False, f"Clínica {cod_clinica} não encontrada", None
                
                doc_data = FirestoreModels.get_consulta_model(
                    cpf_paciente, cod_medico, cod_clinica, data_hora,
                    paciente_data, medico_data, clinica_data, observacoes, status
                )
            else:
                # Modo referenced - apenas verificar se existem
                if not self.buscar_paciente(cpf_paciente):
                    return False, f"Paciente {cpf_paciente} não encontrado", None
                if not self.buscar_medico(cod_medico):
                    return False, f"Médico {cod_medico} não encontrado", None
                if not self.buscar_clinica(cod_clinica):
                    return False, f"Clínica {cod_clinica} não encontrada", None
                
                doc_data = FirestoreModels.get_consulta_model(
                    cpf_paciente, cod_medico, cod_clinica, data_hora,
                    None, None, None, observacoes, status
                )
            
            # Criar com ID automático
            return self.db.create_document_auto_id('consultas', doc_data)
        
        except Exception as e:
            logger.error(f"Erro ao criar consulta: {e}")
            return False, str(e), None
    
    def buscar_consulta(self, consulta_id: str) -> Optional[Dict[str, Any]]:
        """Busca uma consulta por ID"""
        return self.db.get_document('consultas', consulta_id)
    
    def listar_consultas(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista todas as consultas"""
        return self.db.get_all_documents('consultas', limit)
    
    def buscar_consultas_por_paciente(self, cpf_paciente: str) -> List[Dict[str, Any]]:
        """
        Busca consultas de um paciente.
        Funciona tanto em modo embedded quanto referenced.
        """
        if FirebaseConfig.MODELING_MODE == 'embedded':
            filters = FirestoreQueries.consultas_por_paciente_embedded(cpf_paciente)
        else:
            filters = FirestoreQueries.consultas_por_paciente_referenced(cpf_paciente)
        return self.db.query_documents('consultas', filters)
    
    def buscar_consultas_por_medico(self, cod_medico: str) -> List[Dict[str, Any]]:
        """
        Busca consultas de um médico.
        Funciona tanto em modo embedded quanto referenced.
        """
        if FirebaseConfig.MODELING_MODE == 'embedded':
            filters = FirestoreQueries.consultas_por_medico_embedded(cod_medico)
        else:
            filters = FirestoreQueries.consultas_por_medico_referenced(cod_medico)
        return self.db.query_documents('consultas', filters)
    
    def buscar_consultas_por_status(self, status: str) -> List[Dict[str, Any]]:
        """Busca consultas por status (agendada, realizada, cancelada)"""
        filters = FirestoreQueries.consultas_por_status(status)
        return self.db.query_documents('consultas', filters)
    
    def atualizar_consulta(self, consulta_id: str, dados: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Atualiza uma consulta.
        
        Args:
            consulta_id: ID da consulta
            dados: Dados a atualizar
        
        Returns:
            Tuple[bool, str]: (sucesso, mensagem)
        """
        from datetime import datetime
        dados['updated_at'] = datetime.now()
        return self.db.update_document('consultas', consulta_id, dados, merge=True)
    
    def deletar_consulta(self, consulta_id: str) -> Tuple[bool, str]:
        """Deleta uma consulta"""
        return self.db.delete_document('consultas', consulta_id)
    
    # ==================== OPERAÇÕES AVANÇADAS ====================
    
    def contar_consultas_por_especialidade(self) -> Dict[str, int]:
        """
        Conta quantas consultas existem por especialidade médica.
        Funciona apenas em modo embedded.
        
        Returns:
            Dict[str, int]: {especialidade: quantidade}
        """
        if FirebaseConfig.MODELING_MODE != 'embedded':
            logger.warning("Agregação por especialidade funciona melhor em modo embedded")
            return {}
        
        consultas = self.listar_consultas()
        contagem = {}
        
        for consulta in consultas:
            especialidade = consulta.get('medico', {}).get('especialidade', 'Desconhecida')
            contagem[especialidade] = contagem.get(especialidade, 0) + 1
        
        return contagem
    
    def estatisticas_gerais(self) -> Dict[str, Any]:
        """
        Retorna estatísticas gerais do sistema.
        
        Returns:
            Dict com contadores de cada coleção
        """
        return {
            'total_pacientes': self.db.count_documents('pacientes'),
            'total_medicos': self.db.count_documents('medicos'),
            'total_clinicas': self.db.count_documents('clinicas'),
            'total_consultas': self.db.count_documents('consultas'),
            'modo_modelagem': FirebaseConfig.MODELING_MODE
        }


# Instância global
crud = FirestoreCRUD()

"""
Modelos e estruturas de dados para Firebase Firestore
Sistema de Consultório Médico - NoSQL Integration
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from nosql.config_nosql import FirebaseConfig


class FirestoreModels:
    """
    Define a estrutura dos documentos no Firestore.
    Suporta dois modos: embedded (dados completos) e referenced (referências).
    """
    
    @staticmethod
    def paciente_to_firestore(cpf: str, nome: str, data_nascimento: str, 
                               genero: str, telefone: str, email: str) -> Dict[str, Any]:
        """
        Converte dados de paciente do MySQL para formato Firestore.
        
        Args:
            cpf: CPF do paciente (usado como document_id)
            nome: Nome completo
            data_nascimento: Data de nascimento (formato: YYYY-MM-DD)
            genero: M ou F
            telefone: Telefone
            email: Email
        
        Returns:
            Dict: Documento formatado para Firestore
        """
        return {
            'cpf': cpf,
            'nome': nome,
            'data_nascimento': data_nascimento,
            'genero': genero,
            'contato': {
                'telefone': telefone,
                'email': email
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def medico_to_firestore(codigo: str, nome: str, genero: str, 
                           telefone: str, email: str, especialidade: str) -> Dict[str, Any]:
        """
        Converte dados de médico do MySQL para formato Firestore.
        
        Args:
            codigo: Código do médico (usado como document_id)
            nome: Nome completo
            genero: M ou F
            telefone: Telefone
            email: Email
            especialidade: Especialidade médica
        
        Returns:
            Dict: Documento formatado para Firestore
        """
        return {
            'codigo': codigo,
            'nome': nome,
            'genero': genero,
            'especialidade': especialidade,
            'contato': {
                'telefone': telefone,
                'email': email
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def clinica_to_firestore(codigo: str, nome: str, endereco: str, 
                            telefone: str, email: str) -> Dict[str, Any]:
        """
        Converte dados de clínica do MySQL para formato Firestore.
        
        Args:
            codigo: Código da clínica (usado como document_id)
            nome: Nome da clínica
            endereco: Endereço completo
            telefone: Telefone
            email: Email
        
        Returns:
            Dict: Documento formatado para Firestore
        """
        return {
            'codigo': codigo,
            'nome': nome,
            'endereco': endereco,
            'contato': {
                'telefone': telefone,
                'email': email
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def consulta_to_firestore_embedded(cpf_paciente: str, cod_medico: str, cod_clinica: str,
                                       data_hora: str, paciente_data: Dict[str, Any],
                                       medico_data: Dict[str, Any], clinica_data: Dict[str, Any],
                                       observacoes: str = "", status: str = "agendada") -> Dict[str, Any]:
        """
        Cria consulta no modo EMBEDDED (todos os dados em um único documento).
        Vantagem: 1 única query para obter todos os dados.
        Desvantagem: Redundância de dados.
        
        Args:
            cpf_paciente: CPF do paciente
            cod_medico: Código do médico
            cod_clinica: Código da clínica
            data_hora: Data e hora da consulta
            paciente_data: Dados completos do paciente
            medico_data: Dados completos do médico
            clinica_data: Dados completos da clínica
            observacoes: Observações da consulta
            status: Status da consulta (agendada, realizada, cancelada)
        
        Returns:
            Dict: Documento de consulta com dados embedded
        """
        return {
            'data_hora': data_hora,
            'status': status,
            'observacoes': observacoes,
            
            # Dados do paciente embedded
            'paciente': {
                'cpf': cpf_paciente,
                'nome': paciente_data.get('nome', ''),
                'data_nascimento': paciente_data.get('data_nascimento', ''),
                'genero': paciente_data.get('genero', ''),
                'telefone': paciente_data.get('contato', {}).get('telefone', ''),
                'email': paciente_data.get('contato', {}).get('email', '')
            },
            
            # Dados do médico embedded
            'medico': {
                'codigo': cod_medico,
                'nome': medico_data.get('nome', ''),
                'especialidade': medico_data.get('especialidade', ''),
                'telefone': medico_data.get('contato', {}).get('telefone', ''),
                'email': medico_data.get('contato', {}).get('email', '')
            },
            
            # Dados da clínica embedded
            'clinica': {
                'codigo': cod_clinica,
                'nome': clinica_data.get('nome', ''),
                'endereco': clinica_data.get('endereco', ''),
                'telefone': clinica_data.get('contato', {}).get('telefone', ''),
                'email': clinica_data.get('contato', {}).get('email', '')
            },
            
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def consulta_to_firestore_referenced(cpf_paciente: str, cod_medico: str, cod_clinica: str,
                                         data_hora: str, observacoes: str = "", 
                                         status: str = "agendada") -> Dict[str, Any]:
        """
        Cria consulta no modo REFERENCED (apenas referências, como FK do MySQL).
        Vantagem: Sem redundância, dados normalizados.
        Desvantagem: Precisa de múltiplas queries (ou lookup) para obter dados completos.
        
        Args:
            cpf_paciente: CPF do paciente (referência)
            cod_medico: Código do médico (referência)
            cod_clinica: Código da clínica (referência)
            data_hora: Data e hora da consulta
            observacoes: Observações da consulta
            status: Status da consulta
        
        Returns:
            Dict: Documento de consulta com referências
        """
        return {
            'data_hora': data_hora,
            'status': status,
            'observacoes': observacoes,
            
            # Referências (similar a FK do MySQL)
            'paciente_id': cpf_paciente,
            'medico_id': cod_medico,
            'clinica_id': cod_clinica,
            
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    
    @staticmethod
    def get_consulta_model(cpf_paciente: str, cod_medico: str, cod_clinica: str,
                          data_hora: str, paciente_data: Optional[Dict] = None,
                          medico_data: Optional[Dict] = None, clinica_data: Optional[Dict] = None,
                          observacoes: str = "", status: str = "agendada") -> Dict[str, Any]:
        """
        Cria consulta de acordo com o modo configurado (embedded ou referenced).
        
        Returns:
            Dict: Documento de consulta no formato configurado
        """
        if FirebaseConfig.MODELING_MODE == 'embedded':
            if not all([paciente_data, medico_data, clinica_data]):
                raise ValueError("Modo embedded requer dados completos de paciente, médico e clínica")
            return FirestoreModels.consulta_to_firestore_embedded(
                cpf_paciente, cod_medico, cod_clinica, data_hora,
                paciente_data, medico_data, clinica_data, observacoes, status
            )
        else:  # referenced
            return FirestoreModels.consulta_to_firestore_referenced(
                cpf_paciente, cod_medico, cod_clinica, data_hora, observacoes, status
            )


class FirestoreQueries:
    """Queries úteis para o Firestore"""
    
    @staticmethod
    def build_filter(field: str, operator: str, value: Any) -> tuple:
        """
        Constrói um filtro para query.
        
        Args:
            field: Nome do campo
            operator: Operador ('==', '!=', '<', '<=', '>', '>=', 'in', 'array_contains')
            value: Valor a comparar
        
        Returns:
            tuple: (field, operator, value)
        """
        return (field, operator, value)
    
    @staticmethod
    def medicos_por_especialidade(especialidade: str) -> List[tuple]:
        """Filtro para buscar médicos por especialidade"""
        return [FirestoreQueries.build_filter('especialidade', '==', especialidade)]
    
    @staticmethod
    def consultas_por_status(status: str) -> List[tuple]:
        """Filtro para buscar consultas por status"""
        return [FirestoreQueries.build_filter('status', '==', status)]
    
    @staticmethod
    def consultas_por_medico_referenced(cod_medico: str) -> List[tuple]:
        """Filtro para buscar consultas de um médico (modo referenced)"""
        return [FirestoreQueries.build_filter('medico_id', '==', cod_medico)]
    
    @staticmethod
    def consultas_por_medico_embedded(cod_medico: str) -> List[tuple]:
        """Filtro para buscar consultas de um médico (modo embedded)"""
        return [FirestoreQueries.build_filter('medico.codigo', '==', cod_medico)]
    
    @staticmethod
    def consultas_por_paciente_referenced(cpf_paciente: str) -> List[tuple]:
        """Filtro para buscar consultas de um paciente (modo referenced)"""
        return [FirestoreQueries.build_filter('paciente_id', '==', cpf_paciente)]
    
    @staticmethod
    def consultas_por_paciente_embedded(cpf_paciente: str) -> List[tuple]:
        """Filtro para buscar consultas de um paciente (modo embedded)"""
        return [FirestoreQueries.build_filter('paciente.cpf', '==', cpf_paciente)]

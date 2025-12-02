"""
Configurações para Firebase Firestore
Sistema de Consultório Médico - NoSQL Integration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class FirebaseConfig:
    """Configurações do Firebase/Firestore"""
    
    # Caminho para o arquivo de credenciais do Firebase
    # Deve estar no formato JSON baixado do Firebase Console
    FIREBASE_CREDENTIALS_PATH = os.getenv(
        'FIREBASE_CREDENTIALS_PATH',
        str(Path(__file__).parent.parent / 'firebase-credentials.json')
    )
    
    # Nome do projeto Firebase (opcional, será lido das credenciais)
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', None)
    
    # Configurações das coleções
    COLLECTION_PACIENTES = 'pacientes'
    COLLECTION_MEDICOS = 'medicos'
    COLLECTION_CLINICAS = 'clinicas'
    COLLECTION_CONSULTAS = 'consultas'
    
    # Modo de modelagem: 'embedded' ou 'referenced'
    # embedded: dados completos em cada documento de consulta
    # referenced: usa referências entre coleções (como MySQL FK)
    MODELING_MODE = os.getenv('FIREBASE_MODELING_MODE', 'embedded')
    
    # Habilitar logs detalhados
    DEBUG = os.getenv('FIREBASE_DEBUG', 'false').lower() == 'true'
    
    @staticmethod
    def validate():
        """Valida se as configurações estão corretas"""
        if not os.path.exists(FirebaseConfig.FIREBASE_CREDENTIALS_PATH):
            return False, f"Arquivo de credenciais não encontrado: {FirebaseConfig.FIREBASE_CREDENTIALS_PATH}"
        
        if FirebaseConfig.MODELING_MODE not in ['embedded', 'referenced']:
            return False, f"Modo de modelagem inválido: {FirebaseConfig.MODELING_MODE}. Use 'embedded' ou 'referenced'"
        
        return True, "Configuração válida"


# Exportar configuração
config = FirebaseConfig()

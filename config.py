import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv não disponível no ambiente de sistema; proceder sem carregar .env
    pass

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'consultoriomedico')
    # Modo demo / fallback para SQLite (use .env para controlar)
    DEMO = os.getenv('DEMO', 'false').lower() in ('1', 'true', 'yes')
    DB_USE_SQLITE_FALLBACK = os.getenv('DB_USE_SQLITE_FALLBACK', 'true').lower() in ('1', 'true', 'yes')
    SQLITE_PATH = os.getenv('SQLITE_PATH', os.path.join(os.path.dirname(__file__), 'demo.sqlite'))
    
    @staticmethod
    def get_connection_string():
        return f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
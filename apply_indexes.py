# -*- coding: utf-8 -*-
"""Script para aplicar índices no banco de dados para melhorar performance"""
import mysql.connector
from config import Config
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def apply_indexes():
    """Aplica os índices no banco de dados"""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = conn.cursor()
        
        logger.info("Conectado ao banco de dados")
        logger.info("Aplicando índices...")
        
        # Lê o arquivo de índices
        with open('create_indexes.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Separa e executa cada comando
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
        
        for i, cmd in enumerate(commands, 1):
            try:
                logger.info(f"Executando comando {i}/{len(commands)}...")
                cursor.execute(cmd)
                conn.commit()
                logger.info(f"✓ Comando {i} executado com sucesso")
            except mysql.connector.Error as e:
                if "Duplicate key name" in str(e):
                    logger.info(f"⚠ Índice já existe, pulando...")
                else:
                    logger.error(f"✗ Erro no comando {i}: {e}")
        
        cursor.close()
        conn.close()
        logger.info("✓ Índices aplicados com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao aplicar índices: {e}")
        return False
    
    return True

if __name__ == '__main__':
    apply_indexes()

# -*- coding: utf-8 -*-
"""
Script otimizado para popular MySQL com validação de integridade
"""
from faker import Faker
import random
from datetime import datetime, timedelta
import mysql.connector
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker('pt_BR')

ESPECIALIDADES = [
    'Cardiologia', 'Dermatologia', 'Endocrinologia', 'Gastroenterologia',
    'Ginecologia', 'Neurologia', 'Oftalmologia', 'Ortopedia', 
    'Pediatria', 'Psiquiatria', 'Urologia', 'Oncologia'
]

CLINICAS_NOMES = [
    'Clínica São Lucas', 'Hospital Santa Maria', 'Centro Médico Saúde+',
    'Clínica Vida Nova', 'Hospital Esperança', 'Policlínica Central',
    'Clínica MedCare', 'Centro de Saúde Integrado', 'Hospital Regional',
    'Clínica Bem Estar', 'Hospital Coração de Jesus', 'Centro Médico Excellence'
]

def get_connection():
    """Conecta ao MySQL"""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=False
        )
        logger.info(f"✅ Conectado ao MySQL {Config.DB_NAME}")
        return conn
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {e}")
        return None

def limpar_banco(conn):
    """Limpa todas as tabelas"""
    logger.info("🗑️  Limpando banco de dados...")
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE tabelaconsulta")
        cursor.execute("TRUNCATE TABLE tabelapaciente")
        cursor.execute("TRUNCATE TABLE tabelamedico")
        cursor.execute("TRUNCATE TABLE tabelaclinica")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        logger.info("✅ Banco limpo")
    except Exception as e:
        logger.error(f"❌ Erro ao limpar: {e}")
        conn.rollback()
    finally:
        cursor.close()

def generate_cpf():
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

def generate_cod_medico():
    return ''.join([str(random.randint(0, 9)) for _ in range(7)])

def generate_cod_clinica():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def popular_pacientes(conn, quantidade=200):
    """Popula pacientes"""
    logger.info(f"👥 Inserindo {quantidade} pacientes...")
    cursor = conn.cursor()
    cpfs = []
    sucesso = 0
    
    for i in range(quantidade):
        cpf = generate_cpf()
        while cpf in cpfs:
            cpf = generate_cpf()
        
        nome = fake.name()
        data_nasc = fake.date_of_birth(minimum_age=1, maximum_age=95)
        genero = random.choice(['M', 'F'])
        telefone = fake.phone_number()[:20]  # Limita tamanho
        email = fake.email()[:100]
        
        try:
            cursor.execute("""
                INSERT INTO tabelapaciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cpf, nome, data_nasc, genero, telefone, email))
            cpfs.append(cpf)
            sucesso += 1
        except Exception as e:
            logger.warning(f"Erro ao inserir paciente {cpf}: {e}")
        
        if (i + 1) % 50 == 0:
            conn.commit()
            logger.info(f"  {i + 1}/{quantidade} pacientes processados...")
    
    conn.commit()
    cursor.close()
    logger.info(f"✅ {sucesso}/{quantidade} pacientes inseridos")
    return cpfs

def popular_medicos(conn, quantidade=80):
    """Popula médicos"""
    logger.info(f"⚕️  Inserindo {quantidade} médicos...")
    cursor = conn.cursor()
    codigos = []
    sucesso = 0
    
    for i in range(quantidade):
        cod = generate_cod_medico()
        while cod in codigos:
            cod = generate_cod_medico()
        
        nome = fake.name()
        genero = random.choice(['M', 'F'])
        telefone = fake.phone_number()[:20]
        email = fake.email()[:100]
        especialidade = random.choice(ESPECIALIDADES)
        
        try:
            cursor.execute("""
                INSERT INTO tabelamedico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cod, nome, genero, telefone, email, especialidade))
            codigos.append(cod)
            sucesso += 1
        except Exception as e:
            logger.warning(f"Erro ao inserir médico {cod}: {e}")
        
        if (i + 1) % 20 == 0:
            conn.commit()
            logger.info(f"  {i + 1}/{quantidade} médicos processados...")
    
    conn.commit()
    cursor.close()
    logger.info(f"✅ {sucesso}/{quantidade} médicos inseridos")
    return codigos

def popular_clinicas(conn, quantidade=12):
    """Popula clínicas"""
    logger.info(f"🏥 Inserindo {quantidade} clínicas...")
    cursor = conn.cursor()
    codigos = []
    sucesso = 0
    
    for i in range(min(quantidade, len(CLINICAS_NOMES))):
        cod = generate_cod_clinica()
        while cod in codigos:
            cod = generate_cod_clinica()
        
        nome = CLINICAS_NOMES[i]
        endereco = fake.address().replace('\n', ', ')[:200]
        telefone = fake.phone_number()[:20]
        email = fake.company_email()[:100]
        
        try:
            cursor.execute("""
                INSERT INTO tabelaclinica (CodCli, NomeCli, Endereco, Telefone, Email)
                VALUES (%s, %s, %s, %s, %s)
            """, (cod, nome, endereco, telefone, email))
            codigos.append(cod)
            sucesso += 1
        except Exception as e:
            logger.warning(f"Erro ao inserir clínica {cod}: {e}")
    
    conn.commit()
    cursor.close()
    logger.info(f"✅ {sucesso}/{quantidade} clínicas inseridas")
    return codigos

def popular_consultas(conn, cpfs, codigos_med, codigos_cli, quantidade=1500):
    """Popula consultas"""
    logger.info(f"📅 Inserindo {quantidade} consultas...")
    cursor = conn.cursor()
    data_inicial = datetime.now() - timedelta(days=60)
    sucesso = 0
    
    for i in range(quantidade):
        cpf = random.choice(cpfs)
        cod_med = random.choice(codigos_med)
        cod_cli = random.choice(codigos_cli)
        
        dias_offset = random.randint(0, 120)
        data = data_inicial + timedelta(days=dias_offset)
        
        if random.random() < 0.7:
            while data.weekday() >= 5:
                data += timedelta(days=1)
        
        hora = random.randint(8, 17)
        minuto = random.choice([0, 15, 30, 45])
        data_hora = data.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        
        try:
            cursor.execute("""
                INSERT INTO tabelaconsulta (CodCli, CodMed, CpfPaciente, Data_Hora)
                VALUES (%s, %s, %s, %s)
            """, (cod_cli, cod_med, cpf, data_hora))
            sucesso += 1
        except Exception as e:
            if "Duplicate entry" not in str(e):
                logger.warning(f"Erro ao inserir consulta: {e}")
        
        if (i + 1) % 100 == 0:
            conn.commit()
            logger.info(f"  {i + 1}/{quantidade} consultas processadas...")
    
    conn.commit()
    cursor.close()
    logger.info(f"✅ {sucesso}/{quantidade} consultas inseridas")

def main():
    logger.info("=" * 70)
    logger.info("🚀 POPULANDO MYSQL COM DADOS ARTIFICIAIS")
    logger.info("=" * 70)
    
    conn = get_connection()
    if not conn:
        logger.error("❌ Falha na conexão. Encerrando.")
        return
    
    try:
        limpar_banco(conn)
        
        cpfs = popular_pacientes(conn, 200)
        codigos_med = popular_medicos(conn, 80)
        codigos_cli = popular_clinicas(conn, 12)
        
        if cpfs and codigos_med and codigos_cli:
            popular_consultas(conn, cpfs, codigos_med, codigos_cli, 1500)
        else:
            logger.error("❌ Falha ao obter dados base para consultas")
        
        # Estatísticas finais
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tabelapaciente")
        pac = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tabelamedico")
        med = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tabelaclinica")
        cli = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tabelaconsulta")
        con = cursor.fetchone()[0]
        cursor.close()
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ POPULAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("=" * 70)
        logger.info(f"\n📊 Estatísticas Finais:")
        logger.info(f"   👥 Pacientes:  {pac}")
        logger.info(f"   ⚕️  Médicos:    {med}")
        logger.info(f"   🏥 Clínicas:   {cli}")
        logger.info(f"   📅 Consultas:  {con}")
        logger.info(f"\n   Total de registros: {pac + med + cli + con}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Erro durante população: {e}")
        conn.rollback()
    finally:
        conn.close()
        logger.info("🔒 Conexão fechada")

if __name__ == '__main__':
    main()

"""
Script para popular o banco de dados com dados artificiais para demonstração
Gera pacientes, médicos, clínicas e consultas em massa
"""
from faker import Faker
import random
from datetime import datetime, timedelta
from db import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker('pt_BR')

# Listas para diversidade de dados
ESPECIALIDADES = [
    'Cardiologia', 'Dermatologia', 'Endocrinologia', 'Gastroenterologia',
    'Ginecologia', 'Neurologia', 'Oftalmologia', 'Ortopedia', 
    'Pediatria', 'Psiquiatria', 'Urologia', 'Oncologia',
    'Pneumologia', 'Reumatologia', 'Otorrinolaringologia', 'Nefrologia'
]

CLINICAS_NOMES = [
    'Clínica São Lucas', 'Hospital Santa Maria', 'Centro Médico Saúde+',
    'Clínica Vida Nova', 'Hospital Esperança', 'Policlínica Central',
    'Clínica MedCare', 'Centro de Saúde Integrado', 'Hospital Regional',
    'Clínica Bem Estar', 'Hospital Coração de Jesus', 'Centro Médico Excellence'
]

def generate_cpf():
    """Gera CPF válido (apenas formato, não valida dígitos)"""
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

def generate_cod_medico():
    """Gera código de médico com 7 dígitos"""
    return ''.join([str(random.randint(0, 9)) for _ in range(7)])

def generate_cod_clinica():
    """Gera código de clínica com 6 dígitos"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def populate_pacientes(quantidade=200):
    """Insere pacientes no banco"""
    logger.info(f"Gerando {quantidade} pacientes...")
    cpfs_gerados = set()
    sucesso = 0
    
    for i in range(quantidade):
        cpf = generate_cpf()
        # Evita duplicatas
        while cpf in cpfs_gerados:
            cpf = generate_cpf()
        cpfs_gerados.add(cpf)
        
        nome = fake.name()
        data_nasc = fake.date_of_birth(minimum_age=1, maximum_age=95)
        genero = random.choice(['M', 'F'])
        telefone = fake.phone_number()
        email = fake.email()
        
        query = """
        INSERT INTO tabelapaciente (CpfPaciente, NomePac, DataNascimento, Genero, Telefone, Email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, msg = db.execute_query(query, (cpf, nome, data_nasc, genero, telefone, email))
        
        if success:
            sucesso += 1
        if (i + 1) % 50 == 0:
            logger.info(f"  {i + 1}/{quantidade} pacientes processados...")
    
    logger.info(f"✓ {sucesso} pacientes inseridos com sucesso")
    return list(cpfs_gerados)

def populate_medicos(quantidade=80):
    """Insere médicos no banco"""
    logger.info(f"Gerando {quantidade} médicos...")
    codigos_gerados = set()
    sucesso = 0
    
    for i in range(quantidade):
        cod = generate_cod_medico()
        while cod in codigos_gerados:
            cod = generate_cod_medico()
        codigos_gerados.add(cod)
        
        nome = fake.name()
        genero = random.choice(['M', 'F'])
        telefone = fake.phone_number()
        email = fake.email()
        especialidade = random.choice(ESPECIALIDADES)
        
        query = """
        INSERT INTO tabelamedico (CodMed, NomeMed, Genero, Telefone, Email, Especialidade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        success, msg = db.execute_query(query, (cod, nome, genero, telefone, email, especialidade))
        
        if success:
            sucesso += 1
        if (i + 1) % 20 == 0:
            logger.info(f"  {i + 1}/{quantidade} médicos processados...")
    
    logger.info(f"✓ {sucesso} médicos inseridos com sucesso")
    return list(codigos_gerados)

def populate_clinicas(quantidade=15):
    """Insere clínicas no banco"""
    logger.info(f"Gerando {quantidade} clínicas...")
    codigos_gerados = set()
    sucesso = 0
    
    for i in range(min(quantidade, len(CLINICAS_NOMES))):
        cod = generate_cod_clinica()
        while cod in codigos_gerados:
            cod = generate_cod_clinica()
        codigos_gerados.add(cod)
        
        nome = CLINICAS_NOMES[i]
        endereco = fake.address().replace('\n', ', ')
        telefone = fake.phone_number()
        email = fake.company_email()
        
        query = """
        INSERT INTO tabelaclinica (CodCli, NomeCli, Endereco, Telefone, Email)
        VALUES (%s, %s, %s, %s, %s)
        """
        success, msg = db.execute_query(query, (cod, nome, endereco, telefone, email))
        
        if success:
            sucesso += 1
    
    logger.info(f"✓ {sucesso} clínicas inseridas com sucesso")
    return list(codigos_gerados)

def populate_consultas(cpfs, codigos_med, codigos_cli, quantidade=1000):
    """Insere consultas no banco"""
    logger.info(f"Gerando {quantidade} consultas...")
    sucesso = 0
    
    # Gera datas entre 60 dias atrás e 60 dias à frente
    data_inicial = datetime.now() - timedelta(days=60)
    
    for i in range(quantidade):
        # Seleciona elementos aleatórios
        cpf = random.choice(cpfs)
        cod_med = random.choice(codigos_med)
        cod_cli = random.choice(codigos_cli)
        
        # Gera data/hora aleatória (horário comercial: 8h-18h, dias úteis preferencialmente)
        dias_offset = random.randint(0, 120)
        data = data_inicial + timedelta(days=dias_offset)
        
        # Ajusta para dia útil (70% de chance)
        if random.random() < 0.7:
            while data.weekday() >= 5:  # 5=sábado, 6=domingo
                data += timedelta(days=1)
        
        hora = random.randint(8, 17)
        minuto = random.choice([0, 15, 30, 45])
        data_hora = data.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        
        query = """
        INSERT INTO tabelaconsulta (CodCli, CodMed, CpfPaciente, Data_Hora)
        VALUES (%s, %s, %s, %s)
        """
        success, msg = db.execute_query(query, (cod_cli, cod_med, cpf, data_hora))
        
        if success:
            sucesso += 1
        
        if (i + 1) % 100 == 0:
            logger.info(f"  {i + 1}/{quantidade} consultas processadas...")
    
    logger.info(f"✓ {sucesso} consultas inseridas com sucesso")

def main():
    """Executa o script de população do banco"""
    logger.info("=" * 60)
    logger.info("INICIANDO POPULAÇÃO DO BANCO DE DADOS")
    logger.info("=" * 60)
    
    if not db.ensure_connected():
        logger.error("Erro: não foi possível conectar ao banco de dados")
        return
    
    try:
        # Limpar dados existentes (opcional - comentar se quiser manter dados)
        logger.info("\n⚠️  Limpando dados existentes...")
        db.execute_query("DELETE FROM tabelaconsulta")
        db.execute_query("DELETE FROM tabelapaciente")
        db.execute_query("DELETE FROM tabelamedico")
        db.execute_query("DELETE FROM tabelaclinica")
        logger.info("✓ Dados limpos\n")
        
        # Popula as tabelas
        cpfs = populate_pacientes(quantidade=200)
        codigos_med = populate_medicos(quantidade=80)
        codigos_cli = populate_clinicas(quantidade=12)
        
        if cpfs and codigos_med and codigos_cli:
            populate_consultas(cpfs, codigos_med, codigos_cli, quantidade=1500)
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ POPULAÇÃO DO BANCO CONCLUÍDA COM SUCESSO!")
        logger.info("=" * 60)
        
        # Estatísticas finais
        stats = {
            'pacientes': db.fetch_one("SELECT COUNT(*) as total FROM tabelapaciente"),
            'medicos': db.fetch_one("SELECT COUNT(*) as total FROM tabelamedico"),
            'clinicas': db.fetch_one("SELECT COUNT(*) as total FROM tabelaclinica"),
            'consultas': db.fetch_one("SELECT COUNT(*) as total FROM tabelaconsulta")
        }
        
        logger.info(f"\nEstatísticas:")
        logger.info(f"  Pacientes:  {stats['pacientes']['total'] if stats['pacientes'] else 0}")
        logger.info(f"  Médicos:    {stats['medicos']['total'] if stats['medicos'] else 0}")
        logger.info(f"  Clínicas:   {stats['clinicas']['total'] if stats['clinicas'] else 0}")
        logger.info(f"  Consultas:  {stats['consultas']['total'] if stats['consultas'] else 0}")
        
    except Exception as e:
        logger.error(f"Erro durante a população: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    main()

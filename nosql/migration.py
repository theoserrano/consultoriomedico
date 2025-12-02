"""
Script de migração de dados do MySQL para Firebase Firestore
Sistema de Consultório Médico
"""

import sys
import logging
from typing import Tuple
from db import db as mysql_db
from nosql.db_nosql import firebase_db
from nosql.crud_operations import crud

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class MySQLToFirestoreMigration:
    """Classe para migrar dados do MySQL para Firestore"""
    
    def __init__(self):
        self.stats = {
            'pacientes': {'migrados': 0, 'erros': 0},
            'medicos': {'migrados': 0, 'erros': 0},
            'clinicas': {'migrados': 0, 'erros': 0},
            'consultas': {'migrados': 0, 'erros': 0}
        }
    
    def migrar_pacientes(self) -> Tuple[bool, int, int]:
        """
        Migra pacientes do MySQL para Firestore.
        
        Returns:
            Tuple[bool, int, int]: (sucesso, migrados, erros)
        """
        logger.info("=== Migrando Pacientes ===")
        
        # Buscar pacientes do MySQL
        pacientes = mysql_db.fetch_all("SELECT * FROM tabelapaciente")
        
        if not pacientes:
            logger.warning("Nenhum paciente encontrado no MySQL")
            return True, 0, 0
        
        logger.info(f"Encontrados {len(pacientes)} pacientes no MySQL")
        
        migrados = 0
        erros = 0
        
        for pac in pacientes:
            cpf = pac.get('CpfPaciente')
            nome = pac.get('NomePac', '')
            data_nasc = str(pac.get('DataNascimento', ''))
            genero = pac.get('Genero', 'M')
            telefone = pac.get('Telefone', '')
            email = pac.get('Email', '')
            
            sucesso, msg = crud.criar_paciente(cpf, nome, data_nasc, genero, telefone, email)
            
            if sucesso:
                migrados += 1
                logger.debug(f"✓ Paciente {cpf} migrado")
            else:
                erros += 1
                logger.error(f"✗ Erro ao migrar paciente {cpf}: {msg}")
        
        self.stats['pacientes']['migrados'] = migrados
        self.stats['pacientes']['erros'] = erros
        
        logger.info(f"Pacientes: {migrados} migrados, {erros} erros")
        return erros == 0, migrados, erros
    
    def migrar_medicos(self) -> Tuple[bool, int, int]:
        """Migra médicos do MySQL para Firestore"""
        logger.info("=== Migrando Médicos ===")
        
        medicos = mysql_db.fetch_all("SELECT * FROM tabelamedico")
        
        if not medicos:
            logger.warning("Nenhum médico encontrado no MySQL")
            return True, 0, 0
        
        logger.info(f"Encontrados {len(medicos)} médicos no MySQL")
        
        migrados = 0
        erros = 0
        
        for med in medicos:
            codigo = med.get('CodMed')
            nome = med.get('NomeMed', '')
            genero = med.get('Genero', 'M')
            telefone = med.get('Telefone', '')
            email = med.get('Email', '')
            especialidade = med.get('Especialidade', '')
            
            sucesso, msg = crud.criar_medico(codigo, nome, genero, telefone, email, especialidade)
            
            if sucesso:
                migrados += 1
                logger.debug(f"✓ Médico {codigo} migrado")
            else:
                erros += 1
                logger.error(f"✗ Erro ao migrar médico {codigo}: {msg}")
        
        self.stats['medicos']['migrados'] = migrados
        self.stats['medicos']['erros'] = erros
        
        logger.info(f"Médicos: {migrados} migrados, {erros} erros")
        return erros == 0, migrados, erros
    
    def migrar_clinicas(self) -> Tuple[bool, int, int]:
        """Migra clínicas do MySQL para Firestore"""
        logger.info("=== Migrando Clínicas ===")
        
        clinicas = mysql_db.fetch_all("SELECT * FROM tabelaclinica")
        
        if not clinicas:
            logger.warning("Nenhuma clínica encontrada no MySQL")
            return True, 0, 0
        
        logger.info(f"Encontradas {len(clinicas)} clínicas no MySQL")
        
        migrados = 0
        erros = 0
        
        for cli in clinicas:
            codigo = cli.get('CodCli')
            nome = cli.get('NomeCli', '')
            endereco = cli.get('Endereco', '')
            telefone = cli.get('Telefone', '')
            email = cli.get('Email', '')
            
            sucesso, msg = crud.criar_clinica(codigo, nome, endereco, telefone, email)
            
            if sucesso:
                migrados += 1
                logger.debug(f"✓ Clínica {codigo} migrada")
            else:
                erros += 1
                logger.error(f"✗ Erro ao migrar clínica {codigo}: {msg}")
        
        self.stats['clinicas']['migrados'] = migrados
        self.stats['clinicas']['erros'] = erros
        
        logger.info(f"Clínicas: {migrados} migradas, {erros} erros")
        return erros == 0, migrados, erros
    
    def migrar_consultas(self, limit: int = None) -> Tuple[bool, int, int]:
        """
        Migra consultas do MySQL para Firestore.
        
        Args:
            limit: Limite de consultas a migrar (None = todas)
        """
        logger.info("=== Migrando Consultas ===")
        
        query = "SELECT * FROM tabelaconsulta ORDER BY Data_Hora DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        consultas = mysql_db.fetch_all(query)
        
        if not consultas:
            logger.warning("Nenhuma consulta encontrada no MySQL")
            return True, 0, 0
        
        logger.info(f"Encontradas {len(consultas)} consultas no MySQL")
        
        migrados = 0
        erros = 0
        
        for cons in consultas:
            cpf = cons.get('CpfPaciente')
            cod_med = cons.get('CodMed')
            cod_cli = cons.get('CodCli')
            data_hora = str(cons.get('Data_Hora', ''))
            
            sucesso, msg, doc_id = crud.criar_consulta(
                cpf, cod_med, cod_cli, data_hora, 
                observacoes="Migrado do MySQL", status="realizada"
            )
            
            if sucesso:
                migrados += 1
                logger.debug(f"✓ Consulta migrada: {doc_id}")
            else:
                erros += 1
                logger.error(f"✗ Erro ao migrar consulta: {msg}")
        
        self.stats['consultas']['migrados'] = migrados
        self.stats['consultas']['erros'] = erros
        
        logger.info(f"Consultas: {migrados} migradas, {erros} erros")
        return erros == 0, migrados, erros
    
    def migrar_tudo(self, limite_consultas: int = 100) -> bool:
        """
        Migra todos os dados do MySQL para Firestore.
        
        Args:
            limite_consultas: Limite de consultas a migrar (para evitar sobrecarga)
        
        Returns:
            bool: True se tudo foi migrado com sucesso
        """
        logger.info("\n" + "="*60)
        logger.info("INICIANDO MIGRAÇÃO MYSQL → FIRESTORE")
        logger.info("="*60 + "\n")
        
        # Conectar ao MySQL
        if not mysql_db.ensure_connected():
            logger.error("Erro: Não foi possível conectar ao MySQL")
            return False
        
        logger.info("✓ MySQL conectado")
        
        # Conectar ao Firestore
        if not firebase_db.connect():
            logger.error("Erro: Não foi possível conectar ao Firestore")
            return False
        
        logger.info("✓ Firestore conectado\n")
        
        # Migrar na ordem correta (pacientes, médicos, clínicas, depois consultas)
        sucesso_total = True
        
        # 1. Pacientes
        sucesso, mig, err = self.migrar_pacientes()
        sucesso_total = sucesso_total and sucesso
        
        # 2. Médicos
        sucesso, mig, err = self.migrar_medicos()
        sucesso_total = sucesso_total and sucesso
        
        # 3. Clínicas
        sucesso, mig, err = self.migrar_clinicas()
        sucesso_total = sucesso_total and sucesso
        
        # 4. Consultas (com limite)
        if limite_consultas:
            logger.info(f"Migrando apenas {limite_consultas} consultas mais recentes")
        sucesso, mig, err = self.migrar_consultas(limit=limite_consultas)
        sucesso_total = sucesso_total and sucesso
        
        # Resumo final
        self.print_resumo()
        
        return sucesso_total
    
    def print_resumo(self):
        """Imprime resumo da migração"""
        logger.info("\n" + "="*60)
        logger.info("RESUMO DA MIGRAÇÃO")
        logger.info("="*60)
        
        total_migrados = 0
        total_erros = 0
        
        for tipo, stats in self.stats.items():
            mig = stats['migrados']
            err = stats['erros']
            total_migrados += mig
            total_erros += err
            
            status = "✓" if err == 0 else "✗"
            logger.info(f"{status} {tipo.capitalize()}: {mig} migrados, {err} erros")
        
        logger.info("-" * 60)
        logger.info(f"TOTAL: {total_migrados} registros migrados, {total_erros} erros")
        logger.info("="*60 + "\n")


def main():
    """Função principal para executar a migração"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrar dados MySQL para Firebase Firestore')
    parser.add_argument('--limite-consultas', type=int, default=100,
                       help='Limite de consultas a migrar (padrão: 100)')
    parser.add_argument('--debug', action='store_true',
                       help='Ativar modo debug com logs detalhados')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    migration = MySQLToFirestoreMigration()
    
    try:
        sucesso = migration.migrar_tudo(limite_consultas=args.limite_consultas)
        
        if sucesso:
            logger.info("🎉 Migração concluída com sucesso!")
            sys.exit(0)
        else:
            logger.warning("⚠️ Migração concluída com alguns erros")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("\n⚠️ Migração cancelada pelo usuário")
        sys.exit(2)
    except Exception as e:
        logger.error(f"❌ Erro fatal na migração: {e}")
        sys.exit(3)


if __name__ == '__main__':
    main()

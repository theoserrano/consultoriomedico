import logging
import os
import sqlite3
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from config import Config

# logging
logger = logging.getLogger("consultorio.db")
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
logger.setLevel(logging.INFO)


class Database:
    def __init__(self):
        self.connection = None
        self.use_sqlite = False
        self.sqlite_conn = None

    def _connect_mysql(self):
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            logger.info(f"Conectado ao banco {Config.DB_NAME}@{Config.DB_HOST}:{Config.DB_PORT} como {Config.DB_USER}")
            return self.connection
        except Error as e:
            logger.error(f"Erro ao conectar (MySQL): {e}")
            logger.error("Verifique suas credenciais no arquivo .env (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)")
            return None

    def _connect_sqlite(self):
        path = Config.SQLITE_PATH
        # cria diretório do arquivo SQLite, se necessário
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        except Exception:
            pass

        conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # Garantir UTF-8
        conn.execute("PRAGMA encoding = 'UTF-8'")
        conn.text_factory = str
        # registra funções compatíveis com MySQL usadas nas queries
        try:
            conn.create_function('NOW', 0, lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            conn.create_function('CURDATE', 0, lambda: datetime.now().strftime('%Y-%m-%d'))
        except Exception:
            pass
        self.sqlite_conn = conn
        self.use_sqlite = True
        logger.info(f"Usando fallback SQLite em {path}")
        self._ensure_sqlite_schema()
        return conn

    def _ensure_sqlite_schema(self):
        # cria esquema mínimo para demo se não existir
        try:
            c = self.sqlite_conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS tabelapaciente (
                CpfPaciente TEXT PRIMARY KEY,
                NomePac TEXT,
                DataNascimento TEXT,
                Genero TEXT,
                Telefone TEXT,
                Email TEXT
            );
            """)

            c.execute("""
            CREATE TABLE IF NOT EXISTS tabelamedico (
                CodMed TEXT PRIMARY KEY,
                NomeMed TEXT,
                Genero TEXT,
                Telefone TEXT,
                Email TEXT,
                Especialidade TEXT
            );
            """)

            c.execute("""
            CREATE TABLE IF NOT EXISTS tabelaclinica (
                CodCli INTEGER PRIMARY KEY,
                NomeCli TEXT,
                Endereco TEXT
            );
            """)

            c.execute("""
            CREATE TABLE IF NOT EXISTS tabelaconsulta (
                CodCli INTEGER,
                CodMed TEXT,
                CpfPaciente TEXT,
                Data_Hora TEXT,
                PRIMARY KEY (CodCli, CodMed, CpfPaciente, Data_Hora)
            );
            """)

            self.sqlite_conn.commit()
            c.close()
        except Exception as e:
            logger.error(f"Erro ao criar esquema SQLite: {e}")

    def connect(self):
        # tenta conectar MySQL primeiro, a menos que DEMO force sqlite
        if Config.DEMO and Config.DB_USE_SQLITE_FALLBACK:
            return self._connect_sqlite()

        conn = self._connect_mysql()
        if conn is not None:
            return conn

        # se falhou e fallback permitido, usa sqlite
        if Config.DB_USE_SQLITE_FALLBACK:
            logger.warning("Usando fallback para SQLite por problema no MySQL")
            return self._connect_sqlite()

        return None

    def ensure_connected(self):
        """Garantir que exista uma conexão ativa. Tenta reconectar se necessário."""
        try:
            if self.use_sqlite and self.sqlite_conn:
                return True

            if self.connection and getattr(self.connection, 'is_connected', lambda: False)():
                return True
        except Exception:
            pass

        # tentar reconectar
        conn = self.connect()
        ok = False
        if self.use_sqlite:
            ok = self.sqlite_conn is not None
        else:
            ok = conn is not None and getattr(conn, 'is_connected', lambda: False)()

        if ok:
            logger.info("Conexão disponível")
        else:
            logger.warning("Falha ao obter conexão com o banco")
        return ok

    def _adapt_query_for_sqlite(self, query):
        # substitui placeholders %s por ? para sqlite
        return query.replace('%s', '?')

    def execute_query(self, query, params=None):
        if not self.ensure_connected():
            logger.warning("Tentativa de executar query sem conexão")
            return False, "Sem conexão com o banco de dados"

        if self.use_sqlite:
            try:
                q = self._adapt_query_for_sqlite(query)
                cur = self.sqlite_conn.cursor()
                cur.execute(q, params or ())
                self.sqlite_conn.commit()
                cur.close()
                return True, "Operação realizada com sucesso"
            except Exception as e:
                logger.error(f"Erro SQLite ao executar query: {e}")
                return False, str(e)

        # MySQL path
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return True, "Operação realizada com sucesso"
        except Error as e:
            logger.error(f"Erro ao executar query: {e}")
            return False, str(e)
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def fetch_all(self, query, params=None):
        if not self.ensure_connected():
            logger.warning("Sem conexão com o banco ao buscar dados")
            return []

        if self.use_sqlite:
            try:
                q = self._adapt_query_for_sqlite(query)
                cur = self.sqlite_conn.cursor()
                cur.execute(q, params or ())
                rows = [dict(r) for r in cur.fetchall()]
                cur.close()
                return rows
            except Exception as e:
                logger.error(f"Erro SQLite ao buscar dados: {e}")
                return []

        cursor = self.connection.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            return rows
        except Error as e:
            logger.error(f"Erro ao buscar dados: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def fetch_one(self, query, params=None):
        if not self.ensure_connected():
            logger.warning("Sem conexão com o banco ao buscar dado único")
            return None

        if self.use_sqlite:
            try:
                q = self._adapt_query_for_sqlite(query)
                cur = self.sqlite_conn.cursor()
                cur.execute(q, params or ())
                row = cur.fetchone()
                cur.close()
                return dict(row) if row else None
            except Exception as e:
                logger.error(f"Erro SQLite ao buscar dado único: {e}")
                return None
        
        # MySQL path
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        try:
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            return row
        except Error as e:
            logger.error(f"Erro ao buscar dado único: {e}")
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass

    def fetch_all_paginated(self, query, params=None, limit=None, offset=None):
        """Busca com suporte a LIMIT/OFFSET de forma portável entre MySQL e SQLite.
        Se o query já contiver LIMIT, não adiciona nada.
        """
        if 'LIMIT' in query.upper():
            return self.fetch_all(query, params)

        q = query
        final_params = list(params) if params else []
        if limit is not None:
            if self.use_sqlite:
                q = q.rstrip().rstrip(';') + ' LIMIT ?'
                final_params.append(limit)
                if offset is not None:
                    q += ' OFFSET ?'
                    final_params.append(offset)
            else:
                q = q.rstrip().rstrip(';') + ' LIMIT %s'
                final_params.append(limit)
                if offset is not None:
                    q += ' OFFSET %s'
                    final_params.append(offset)

        return self.fetch_all(q, final_params)

    def get_clinicas(self):
        return self.fetch_all('SELECT CodCli, NomeCli FROM tabelaclinica ORDER BY NomeCli')

    def get_medicos(self):
        return self.fetch_all('SELECT CodMed, NomeMed FROM tabelamedico ORDER BY NomeMed')


    def close(self):
        try:
            if self.use_sqlite and self.sqlite_conn:
                self.sqlite_conn.close()
        except Exception:
            pass


db = Database()
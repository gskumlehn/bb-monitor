import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None

def _cred_path() -> str:
    _logger.info("Obtendo o caminho das credenciais do Google Cloud.")
    path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        _logger.error("GOOGLE_APPLICATION_CREDENTIALS não definido.")
        raise RuntimeError("Defina GOOGLE_APPLICATION_CREDENTIALS")
    if not os.path.isfile(path):
        _logger.error("Arquivo de credenciais não encontrado: %s", os.path.abspath(path))
        raise RuntimeError(f"Arquivo de credenciais não encontrado: {os.path.abspath(path)}")
    _logger.info("Caminho das credenciais obtido: %s", path)
    return path

def _project_id() -> str:
    _logger.info("Obtendo o ID do projeto BigQuery.")
    project = os.getenv("BQ_PROJECT")
    if not project:
        _logger.error("BQ_PROJECT não definido no .env.")
        raise RuntimeError("BQ_PROJECT não definido no .env.")
    _logger.info("ID do projeto BigQuery obtido: %s", project)
    return project

def get_engine():
    global _engine
    if _engine is not None:
        _logger.info("Engine BigQuery já existente. Retornando engine existente.")
        return _engine
    _logger.info("Criando nova engine BigQuery.")
    credentials_path = _cred_path()
    project = _project_id()
    conn_str = f"bigquery://{project}"
    _logger.info("String de conexão BigQuery: %s", conn_str)
    engine_kwargs = {"credentials_path": credentials_path}
    try:
        _engine = create_engine(conn_str, pool_pre_ping=True, **engine_kwargs)
        _logger.info("Engine BigQuery criada com sucesso.")
    except Exception as e:
        _logger.error("Erro ao criar a engine BigQuery: %s", str(e))
        raise
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is not None:
        _logger.info("SessionLocal já existente. Retornando sessão existente.")
        return _SessionLocal
    _logger.info("Criando nova SessionLocal.")
    engine = get_engine()
    try:
        _SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
        _logger.info("SessionLocal criada com sucesso.")
    except Exception as e:
        _logger.error("Erro ao criar SessionLocal: %s", str(e))
        raise
    return _SessionLocal

@contextmanager
def get_session():
    _logger.info("Iniciando uma nova sessão.")
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        _logger.info("Sessão iniciada com sucesso.")
        yield db
        _logger.info("Commitando a sessão.")
        db.commit()
    except Exception as e:
        _logger.error("Erro durante a execução da sessão: %s", str(e))
        _logger.info("Realizando rollback da sessão.")
        db.rollback()
        raise
    finally:
        _logger.info("Fechando a sessão.")
        db.close()

# app/infra/bq_sa.py
import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None

def _resolve_project_id() -> str:
    project = os.getenv("BQ_PROJECT")
    if not project:
        raise RuntimeError("Não foi possível resolver o PROJECT_ID (defina BQ_PROJECT ou GOOGLE_CLOUD_PROJECT).")
    return project

def get_engine():
    global _engine
    if _engine is not None:
        return _engine

    project = _resolve_project_id()

    conn_str = f"bigquery://{project}"
    _logger.info("Criando engine BigQuery para projeto: %s", project)
    _engine = create_engine(conn_str, pool_pre_ping=True)

    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is not None:
        return _SessionLocal

    engine = get_engine()
    _SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return _SessionLocal

@contextmanager
def get_session():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

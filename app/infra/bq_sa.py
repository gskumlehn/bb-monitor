# app/infra/bq_sa.py
import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Caches
_engine = None
_SessionLocal = None

def _require_project() -> str:
    project = os.getenv("BQ_PROJECT")
    if not project:
        raise RuntimeError("Defina a variável de ambiente BQ_PROJECT")
    return project

def get_engine():
    """
    Retorna um Engine singleton do SQLAlchemy usando o dialeto BigQuery.
    A autenticação é resolvida pelo Google Auth Default:
      - GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account.json
      - ou ADC da máquina
    """
    global _engine
    if _engine is not None:
        return _engine

    project = _require_project()
    # NÃO passe 'credentials=' para o create_engine. O dialeto já resolve via ADC.
    _engine = create_engine(
        f"bigquery://{project}",
        pool_pre_ping=True,  # mais robusto
    )
    return _engine

def get_session_local():
    """
    Retorna um sessionmaker singleton.
    """
    global _SessionLocal
    if _SessionLocal is not None:
        return _SessionLocal

    engine = get_engine()
    _SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return _SessionLocal

@contextmanager
def get_session() -> Iterator[Session]:
    """
    Context manager que abre Session, faz commit ao sair
    (se não houver exceção), rollback se falhar, e sempre fecha.
    """
    SessionLocal = get_session_local()
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

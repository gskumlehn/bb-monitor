import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_SessionLocal = None

def _cred_path() -> str:
    path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise RuntimeError("Defina GOOGLE_APPLICATION_CREDENTIALS")
    return path

def _project_id() -> str:
    project = os.getenv("BQ_PROJECT")
    if not project:
        raise RuntimeError("BQ_PROJECT não definido no .env.")
    return project

def get_engine():
    global _engine
    if _engine is not None:
        return _engine
    credentials_path = _cred_path()
    project = _project_id()
    conn_str = f"bigquery://{project}"
    engine_kwargs = {"credentials_path": credentials_path}
    try:
        _engine = create_engine(conn_str, pool_pre_ping=True, **engine_kwargs)
    except Exception as e:
        raise
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is not None:
        return _SessionLocal
    engine = get_engine()
    try:
        _SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    except Exception as e:
        raise
    return _SessionLocal

@contextmanager
def get_session():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

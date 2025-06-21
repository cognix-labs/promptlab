from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

_engine = None
_SessionLocal = None

def init_engine(db_url):
    global _engine, _SessionLocal
    _engine = create_engine(db_url, connect_args={"check_same_thread": False})
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    Base.metadata.create_all(bind=_engine)

def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Session not initialized. Call init_engine first.")
    return _SessionLocal()

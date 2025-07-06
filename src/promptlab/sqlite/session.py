from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

_engine = None
_SessionLocal = None


def _create_default_admin_user():
    """Create default admin user if it doesn't exist."""
    from .models import User
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    session = _SessionLocal()
    try:
        if not session.query(User).filter_by(username="admin").first():
            admin_user = User(
                username="admin", password_hash=pwd_context.hash("admin"), role="admin"
            )
            session.add(admin_user)
            session.commit()
    finally:
        session.close()


def init_engine(db_url):
    global _engine, _SessionLocal
    _engine = create_engine(db_url, connect_args={"check_same_thread": False})
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    Base.metadata.create_all(bind=_engine)

    # Insert default admin user if not exists
    _create_default_admin_user()


def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Session not initialized. Call init_engine first.")
    return _SessionLocal()

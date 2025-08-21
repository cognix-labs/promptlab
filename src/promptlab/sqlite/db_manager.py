import threading
import logging
from pathlib import Path
from requests import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from alembic.config import Config
from alembic import command
from .models import User
from passlib.context import CryptContext

import threading
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self._engine = None
        self._session = None
        self._db_initialized = False
        self._init_lock = threading.Lock()

    def initialize_database(self, db_file: str) -> None:
        """Initialize the database and run migrations, create default admin user."""
        if self._db_initialized:
            logger.info("Database already initialized, skipping initialization")
            return
        
        db_path = Path(db_file)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_url = f"sqlite:///{db_file}"
        logger.info(f"Initializing database at: {db_file}")

        try:
            self._init_engine(db_url)
            self._run_migrations(db_url)
            self._create_default_admin_user()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def _init_engine(self, db_url):
        """Initialize the database engine and session maker (thread-safe, idempotent)."""
        if self._db_initialized:
            return
        with self._init_lock:
            if self._db_initialized:
                return
            self._engine = create_engine(db_url, connect_args={"check_same_thread": False})
            self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
            self._db_initialized = True

    def get_session(self):
        """Return a new SQLAlchemy session."""
        if self._session is None:
            raise RuntimeError("Session not initialized. Call init_engine first.")
        return self._session()

    def _create_default_admin_user(self):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        try:
            session = self.get_session()
            if not session.query(User).filter_by(username="admin").first():
                admin_user = User(
                    username="admin", password_hash=pwd_context.hash("admin"), role="admin"
                )
                session.add(admin_user)
                session.commit()
        finally:
            session.close()

    def _run_migrations(self, db_url: str) -> None:
        try:
            package_root = Path(__file__).parent.parent
            alembic_cfg_path = package_root / "alembic.ini"
            if not alembic_cfg_path.exists():
                logger.warning("Alembic configuration not found, skipping migrations")
                return
            
            alembic_cfg = Config(str(alembic_cfg_path))
            alembic_cfg.set_main_option("sqlalchemy.url", db_url)
            script_location = alembic_cfg.get_main_option("script_location")

            if script_location and not Path(script_location).is_absolute():
                abs_script_location = str((alembic_cfg_path.parent / script_location).resolve())
                alembic_cfg.set_main_option("script_location", abs_script_location)

            logger.info("Running Alembic migrations to update database schema...")
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations applied successfully.")
        except ImportError:
            logger.warning("Alembic not installed, skipping migrations")
        except Exception as e:
            logger.error(f"Error running migrations: {e}")

db_manager = DatabaseManager()

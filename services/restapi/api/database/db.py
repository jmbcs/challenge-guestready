import logging
from contextlib import contextmanager
from typing import Any, Generator

from api.settings import config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

log: logging.Logger = logging.getLogger(__name__)


# Base class for declarative class definitions
class Base(DeclarativeBase):
    pass


# Create an engine instance
engine: Engine = create_engine(config.db.get_url(), echo=True)

# Create a configured "Session" class
SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Provide a context manager for session handling
@contextmanager
def get_db_session() -> Generator[Session, Any, None]:
    """
    Provide a transactional scope around a series of operations.
    This ensures that sessions are properly closed after use.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        log.error(f"Session rollback due to: {e}")
        raise e
    finally:
        session.close()


# Dependency to get the database session
def get_db() -> Generator[Session, Any, None]:
    with get_db_session() as db:
        yield db
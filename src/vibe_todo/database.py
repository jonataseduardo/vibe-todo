"""Database module for SQLModel ORM setup and session management."""

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

from vibe_todo.logger import logger

# Import all models to register them with SQLModel metadata
from vibe_todo.models import MyDayTask, Subtask, Task, TodoList  # noqa: F401

# Database connection string
DATABASE_URL = "sqlite:///data/todos.db"

# Global engine instance (singleton pattern)
_engine = None


def get_engine():
    """
    Get or create database engine using singleton pattern.

    Returns:
        Engine: SQLModel engine instance
    """
    global _engine
    if _engine is None:
        try:
            # Ensure data directory exists
            db_path = Path("data")
            db_path.mkdir(exist_ok=True)
            logger.info(f"Database directory ensured: {db_path.absolute()}")

            # Create engine
            _engine = create_engine(
                DATABASE_URL,
                echo=False,  # Set to True for SQL query logging
                connect_args={"check_same_thread": False},  # Required for SQLite with multiple threads
            )
            logger.info(f"Database engine created successfully: {DATABASE_URL}")
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise
    return _engine


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Create a database session context manager.

    Yields:
        Session: SQLModel session instance

    Example:
        with get_session() as session:
            # Use session for database operations
            pass
    """
    engine = get_engine()
    session = Session(engine)
    try:
        logger.debug("Database session created")
        yield session
        session.commit()
        logger.debug("Database session committed")
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error, rolling back: {e}")
        raise
    finally:
        session.close()
        logger.debug("Database session closed")


def create_db_and_tables() -> None:
    """
    Create database and all tables defined in SQLModel models.

    This function should be called on application startup to ensure
    the database schema is initialized. Also initializes system lists.
    """
    try:
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")

        # Initialize system lists
        from vibe_todo.services import initialize_system_lists

        with get_session() as session:
            initialize_system_lists(session)
            logger.info("System lists initialized successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

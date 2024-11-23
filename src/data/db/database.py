from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.pool import StaticPool
import os
from contextlib import contextmanager
from src.core.config import logger

# Create the base class for declarative models
Base = declarative_base()

# Create engine (using SQLite for simplicity)
DATABASE_URL = "sqlite:///./learnicity.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL query logging
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def get_db() -> Session:
    """Get database session with automatic closing
    
    Returns:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        logger.error(f"Error getting database session: {str(e)}")
        raise

@contextmanager
def get_db_context():
    """Context manager for database sessions
    
    Usage:
        with get_db_context() as db:
            db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

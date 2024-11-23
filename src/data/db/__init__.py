from .db import Database
from src.core.config import logger

db = Database()

async def init_db():
    """Initialize database connection"""
    if not db.is_connected:
        try:
            await db.connect()
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            raise
    else:
        logger.info("Database already connected")

__all__ = ["db", "init_db"]
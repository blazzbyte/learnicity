from prisma import Prisma
from src.core.config import logger

# Database connection singleton
class Database:
    """Singleton class to manage database connection"""
    _instance = None
    _db = None
    _is_connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._db = Prisma()
        return cls._instance

    async def init_db(self):
        """Initialize database connection"""
        if not self._is_connected:
            try:
                await self.connect()
                logger.info("Database connected successfully")
            except Exception as e:
                logger.error(f"Error connecting to database: {str(e)}")
                raise

    async def connect(self):
        """Establish connection to the database if not already connected"""
        if not self._is_connected:
            await self._db.connect()
            self._is_connected = True

    async def disconnect(self):
        """Close the database connection if connected"""
        if self._is_connected:
            await self._db.disconnect()
            self._is_connected = False

    @property
    def prisma(self):
        """Get the Prisma client instance"""
        return self._db

    @property
    def is_connected(self):
        """Check if database is connected"""
        return self._is_connected

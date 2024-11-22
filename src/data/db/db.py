from prisma import Prisma

# Database connection singleton
class Database:
    """Singleton class to manage database connection"""
    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._db = Prisma()
        return cls._instance

    async def connect(self):
        """Establish connection to the database if not already connected"""
        if not self._db.is_connected():
            await self._db.connect()

    async def disconnect(self):
        """Close the database connection if connected"""
        if self._db.is_connected():
            await self._db.disconnect()

    @property
    def prisma(self):
        """Get the Prisma client instance"""
        return self._db

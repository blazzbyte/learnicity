import uuid
from sqlalchemy import Column, String
from src.data.db.database import Base

class User(Base):
    """User model with unique identifier"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        """Converts the user instance to a dictionary format
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            "id": self.id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Creates a new User instance from a dictionary
        
        Args:
            data (dict): Dictionary containing user data
            
        Returns:
            User: New User instance
        """
        return cls(id=data.get("id"))

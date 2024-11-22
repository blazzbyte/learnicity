from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass
class User:
    """User model with unique identifier"""
    id: UUID = uuid4()

    def to_dict(self) -> dict:
        """Converts the user instance to a dictionary format
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            "id": str(self.id)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Creates a new User instance from a dictionary
        
        Args:
            data (dict): Dictionary containing user data
            
        Returns:
            User: New User instance
        """
        return cls(
            id=UUID(data["id"]) if isinstance(data["id"], str) else data["id"]
        )

from typing import Optional

from src.data.models.user import User
from src.data.db import get_db

from src.core.config import logger


class UserService:
    def __init__(self):
        self.db = get_db()

    def create_user(self) -> User:
        """Create a new user in the database

        Returns:
            User: The created user instance
        """
        try:
            user = User()
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise

    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user from the database by ID

        Args:
            user_id (str): The user's ID to look for

        Returns:
            Optional[User]: The user if found, None otherwise
        """
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None

    def delete_user(self, user_id: str) -> bool:
        """Delete a user from the database

        Args:
            user_id (str): The ID of the user to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                self.db.delete(user)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user: {str(e)}")
            return False

import src.db.db_client as db_c

from abc import abstractmethod, ABC
from src.data import UserDTO, User


class UserService(ABC):

    def __init__(self, db_client: 'db_c.SoflyDbClient'):
        """
        Initialize the UserService.
        """
        self.db_client = db_client

    @abstractmethod
    async def create_user(self, user_data: UserDTO) -> bool:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        """Get all users."""
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        pass

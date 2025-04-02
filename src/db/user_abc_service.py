from abc import abstractmethod, ABC
from src.data import UserDTO, User


class UserService(ABC):

    @abstractmethod
    def create_user(self, user_data: UserDTO) -> bool:
        """Create a new user."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID."""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email."""
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        """Get all users."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

from src.data import User, UserDTO
from src.db import UserService


class UserSoflyService(UserService):

    def create_user(self, user_data: UserDTO) -> bool:
        pass

    def get_user_by_id(self, user_id: int) -> User | None:
        pass

    def get_user_by_username(self, username: str) -> User | None:
        pass

    def get_user_by_email(self, email: str) -> User | None:
        pass

    def get_all_users(self) -> list[User]:
        pass

    def delete_user(self, user_id: int) -> bool:
        pass
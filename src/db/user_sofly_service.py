from loguru import logger
from pymysql import IntegrityError

import src.db.db_client as db_c

from src.data import User, UserDTO
from src.db.user_abc_service import UserService


class UserSoflyService(UserService):

    def __init__(self, db_client: 'db_c.SoflyDbClient'):
        """
        Initialize the UserSoflyService with a database client.
        """
        super().__init__(db_client)

    def create_user(self, user_data: UserDTO) -> bool:
        try:
            result = self.db_client.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                user_data.username, user_data.email, user_data.password_hash
            )
            return result == 1
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            return False
        except Exception as e:
            logger.error(f"Exception: {e}")
            return False

    def get_user_by_id(self, user_id: int) -> User | None:
        result = self.db_client.fetch(
            "SELECT * FROM users WHERE id = %s",
            user_id
        )

        if result:
            user = result[0]
            return User(
                user_id=user['id'],
                username=user['username'],
                email=user['email'],
                password_hash=user['password_hash']
            )
        return None

    def get_user_by_username(self, username: str) -> User | None:
        result = self.db_client.fetch(
            "SELECT * FROM users WHERE username = %s",
            username
        )

        if result:
            user = result[0]
            return User(
                user_id=user['id'],
                username=user['username'],
                email=user['email'],
                password_hash=user['password_hash']
            )

        return None

    def get_user_by_email(self, email: str) -> User | None:
        result = self.db_client.fetch(
            "SELECT * FROM users WHERE email = %s",
            email
        )

        if result:
            user = result[0]
            return User(
                user_id=user['id'],
                username=user['username'],
                email=user['email'],
                password_hash=user['password_hash']
            )
        return None

    def get_all_users(self) -> list[User]:
        result = self.db_client.fetch(
            "SELECT * FROM users"
        )

        users = []
        for user in result:
            users.append(
                User(
                    user_id=user['id'],
                    username=user['username'],
                    email=user['email'],
                    password_hash=user['password_hash']
                )
            )
        return users

    def delete_user(self, user_id: int) -> bool:
        result = self.db_client.execute(
            "DELETE FROM users WHERE id = %s",
            user_id
        )

        return result.rowcount == 1

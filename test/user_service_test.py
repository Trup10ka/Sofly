import unittest

from src.config.pyhocon_config_loader import PyhoconConfigLoader
from src.data import UserDTO
from src.db import SoflyDbClient


class UserServiceTest(unittest.TestCase):

    def test_is_user_added_if_all_parameters_are_correct(self):
        config = PyhoconConfigLoader("../config.conf").load_config()

        if config is None:
            raise ValueError("Configuration file not found or invalid.")
        if config.database is None:
            raise ValueError("Database configuration not found in the configuration file.")

        db_client = SoflyDbClient(config.database)
        db_client.init_db_client()

        db_client.user_service.create_user(UserDTO(
            "jirkakral", "jirkakral@seznam.cz", "password123"
        ))

        user = db_client.user_service.get_user_by_username("jirkakral")

        self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()

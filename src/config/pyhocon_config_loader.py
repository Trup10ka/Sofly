import pyhocon as hoc

import src.config as cf_p
from src.config.config_loader import ConfigLoader
from loguru import logger

class PyhoconConfigLoader(ConfigLoader):
    """
    Class for loading configuration files using the pyhocon library.

    This class is responsible for loading configuration files in HOCON format.
    """
    def load_config(self) -> cf_p.SoflyConfig | int:
        """
        Load the configuration from a Hocon file using pyhocon lib.
        """
        if self.copy_default_confi_if_not_exists():
            logger.warning(f"Default configuration file copied to {self.config_file_path}, program will now exit.")
            return 1

        config = hoc.ConfigFactory.parse_file(self.config_file_path)

        if config is None:
            logger.error("Failed to load configuration file.")
            return -1

        database_host = config.get_string("database.host")
        database_port = config.get_int("database.port")
        database_username = config.get_string("database.username")
        database_password = config.get_string("database.password")
        database_name = config.get_string("database.db_name")

        logging_level = config.get_string("logging.level")
        logging_file_path = config.get_string("logging.file_path")

        server_host = config.get_string("server.host")
        server_port = config.get_int("server.port")

        jwt_secret = config.get_string("jwt-secret")

        sofly_config = cf_p.SoflyConfig(
            database = cf_p.DatabaseConfig(
                database_host,
                database_port,
                database_username,
                database_password,
                database_name
            ),
            logging = cf_p.LoggingConfig(
                logging_level,
                logging_file_path
            ),
            server = cf_p.ServerConfig(
                server_host,
                server_port
            ),
            jwt_secret = jwt_secret
        )
        logger.success("Config loaded successfully.")
        return sofly_config

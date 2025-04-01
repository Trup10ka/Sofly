import pyhocon as hoc

from src.config.config import SoflyConfig
from src.config.config_loader import ConfigLoader

### TYPE ALIAS ###
DatabaseConfig = SoflyConfig.DatabaseConfig
LoggingConfig = SoflyConfig.LoggingConfig
ServerConfig = SoflyConfig.ServerConfig
### END TYPE ALIAS ###

class PyhoconConfigLoader(ConfigLoader):
    """
    Class for loading configuration files using the pyhocon library.

    This class is responsible for loading configuration files in HOCON format.
    """
    def load_config(self) -> SoflyConfig:
        """
        Load the configuration from a Hocon file using pyhocon lib.
        """

        config = hoc.ConfigFactory.parse_file(self.config_file_path)

        database_host = config.get_string("database.host")
        database_port = config.get_int("database.port")
        database_username = config.get_string("database.username")
        database_password = config.get_string("database.password")
        database_name = config.get_string("database.db_name")

        logging_level = config.get_string("logging.level")
        logging_file_path = config.get_string("logging.file_path")

        server_host = config.get_string("server.host")
        server_port = config.get_int("server.port")

        sofly_config = SoflyConfig(
            database = DatabaseConfig(
                database_host,
                database_port,
                database_username,
                database_password,
                database_name
            ),
            logging = LoggingConfig(
                logging_level,
                logging_file_path
            ),
            server = ServerConfig(
                server_host,
                server_port
            )
        )

        return sofly_config

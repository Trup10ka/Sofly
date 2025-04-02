import src.config as cf

class SoflyConfig:

    def __init__(self, database: 'cf.DatabaseConfig' = None, server: 'cf.ServerConfig' = None, logging: 'cf.LoggingConfig' = None, jwt_secret: str = None):
        self.database = database
        self.server = server
        self.logging = logging
        self.jwt_secret = jwt_secret
        self._validate()

    def _validate(self) -> None:
        """
        Validate the configuration sections.

        This function checks if the configuration sections are not None and if they are instances of their respective classes.

        It also checks if the attributes of the configuration sections are not None.

        Throws
        -------
            - ``ValueError`` if any section is None or if any attribute of the sections is None.

            - ``TypeError`` if any section is not an instance of its respective class.
        """
        if any(section is None for section in [self.database, self.server, self.logging]):
            raise ValueError("Configuration sections cannot be None")
        try:
            for section_name, section in [("Database", self.database), ("Logging", self.logging), ("Server", self.server)]:
                for attr, value in vars(section).items():
                    if value is None:
                        raise ValueError(f"{section_name} configuration '{attr}' cannot be None")
        except TypeError:
            raise TypeError("Configuration sections must be instances of their respective classes")

    def __str__(self):
        return f"SoflyConfig(database={self.database}, server={self.server}, logging={self.logging})"

    class DatabaseConfig:
        def __init__(self, host: str = None, port: int = None, username: str = None, password: str = None, db_name: str = None):
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            self.db_name = db_name

        def __str__(self):
            return f"DatabaseConfig(host={self.host}, port={self.port}, username={self.username}, password={self.password}, database={self.db_name})"

    class LoggingConfig:
        def __init__(self, level=None, file_path=None):
            self.level = level
            self.file_path = file_path

        def __str__(self):
            return f"LoggingConfig(level={self.level}, file_path={self.file_path})"

    class ServerConfig:
        def __init__(self, host=None, port=None):
            self.host = host
            self.port = port

        def __str__(self):
            return f"ServerConfig(host={self.host}, port={self.port})"
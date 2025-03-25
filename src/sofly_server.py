import os

from flask import Flask
from loguru import logger


class SoflyServer:
    """
    A class that represents a server instance

    It is recommended to use the builder pattern to create an instance of this class since it has a lot of parameters

    Attributes:
    - host: str | Does not have a default value -> must set
        The host of the server
    - port: int | Default value is 6623
        The port of the server
    - static_folder: str | Default value is 'public'
        The folder where static files are stored
    - template_folder: str | Default value is 'templates'
        The folder where templates/html files are stored
    - is_debug: bool | Default value is True
        Whether the server is in debug mode
    - should_create_public_dir: bool | Default value is True
        Whether the server should create a public directory for static files
    """
    def __new__(cls, *args, **kwargs):
        if any(arg is None for arg in args) or any(value is None for value in kwargs.values()):
            logger.critical("THE SERVER CANNOT BE INSTANTIATED WITHOUT THE REQUIRED ARGUMENTS")
            return None
        return super(SoflyServer, cls).__new__(cls)

    def __init__(self,
                 host: str = '0.0.0.0',
                 port: int = 5000,
                 static_folder: str = 'public',
                 template_folder: str = 'templates',
                 is_debug: bool = True,
                 should_create_public_dir: bool = True) -> None:
        logger.info(f"Creating SoflyServer instance at {static_folder}/{template_folder}")
        self.app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
        logger.success("Created SoflyServer instance")

        self.is_debug = is_debug
        self.should_create_public_dir = should_create_public_dir

    def init(self):
        logger.info("Initializing SoflyServer")
        if self.should_create_public_dir:
            logger.info("Creating a public directory for static files")
            os.makedirs('public', exist_ok=True)
        else:
            logger.warning("Creating of public directory is not allowed, ensure it exists!")

    @classmethod
    def builder(cls):
        return SoflyServerBuilder()

    def run(self) -> None:
        logger.info("Running SoflyServer")
        self.app.run(host='0.0.0.0', port=5000, debug=self.is_debug)


class SoflyServerBuilder:
    def __init__(self):
        self._static_folder = 'public'
        self._template_folder = 'templates'
        self._is_debug = True
        self._should_create_public_dir = True
        self._host = None
        self._port = 6623

    def set_static_folder(self, static_folder: str):
        self._static_folder = static_folder
        return self

    def set_template_folder(self, template_folder: str):
        self._template_folder = template_folder
        return self

    def set_debug(self, is_debug: bool):
        self._is_debug = is_debug
        return self

    def set_public_dir_creation(self, should_create_public_dir: bool):
        self._should_create_public_dir = should_create_public_dir
        return self

    def set_host(self, host: str):
        self._host = host
        return self

    def set_port(self, port: int):
        self._port = port
        return self

    def build(self) -> SoflyServer | None:
        if self._host is None:
            logger.critical(f"You must provide the server with a host - host not provided")
            return None

        return SoflyServer(
            static_folder=self._static_folder,
            template_folder=self._template_folder,
            is_debug=self._is_debug,
            should_create_public_dir=self._should_create_public_dir
        )

import os

import src.sofly_endpoints as sofly_endpoints

from flask import Flask
from loguru import logger

from src.db import SoflyDbClient
from src.security import JWTService


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
    - JWTService: JWTService
        The JWT service to handle token generation and verification
    - DbClient: DbClient
        The database client to interact with the database
    """

    def __new__(cls, *args, **kwargs):
        if any(arg is None for arg in args) or any(value is None for value in kwargs.values()):
            logger.critical("THE SERVER CANNOT BE INSTANTIATED WITHOUT THE REQUIRED ARGUMENTS")
            return None
        return super(SoflyServer, cls).__new__(cls)

    def __init__(self,
                    host: str,
                    jwt_service: JWTService,
                    db_client: SoflyDbClient,
                    ai_model,
                    port: int = 5000,
                    static_folder_path: str = os.path.join(os.getcwd(), 'public'),
                    template_folder: str = os.path.join(os.getcwd(),'templates'),
                    is_debug: bool = True,
                    should_create_public_dir: bool = True,
                 ) -> None:
        logger.info(f"Creating SoflyServer instance with static: {static_folder_path}, templates: {template_folder}")
        self.flask_app = Flask(__name__, static_folder=static_folder_path, template_folder=template_folder)

        self.flask_app.debug = is_debug
        self.host = host
        self.port = port
        self.is_debug = is_debug
        self.should_create_public_dir = should_create_public_dir
        self.jwt_service = jwt_service
        self.db_client = db_client
        self.ai_model = ai_model

        logger.success("Created SoflyServer instance")

    def init(self):
        logger.info("Initializing SoflyServer")
        self.init_static_folder()
        sofly_endpoints.init_endpoints(self)

    def init_static_folder(self):
        logger.info("Initializing static folder")

        if self.should_create_public_dir:
            os.makedirs(self.flask_app.static_folder, exist_ok=True)
            logger.info(f"Ensured static folder exists: {self.flask_app.static_folder}")


    @classmethod
    def builder(cls):
        return SoflyServerBuilder()

    def run(self) -> None:
        logger.info(f"Running SoflyServer on {self.host}:{self.port}")
        self.flask_app.run(host=self.host, port=self.port, debug=self.is_debug)


class SoflyServerBuilder:
    def __init__(self):
        self._static_folder = os.path.join(os.getcwd(), 'public')
        self._template_folder = 'templates'
        self.ai_model = None
        self._db_client = None
        self._jwt_service = None
        self._is_debug = True
        self._should_create_public_dir = True
        self._host = None
        self._port = 6623  # Default port

    def set_static_folder(self, static_folder: str):
        self._static_folder = os.path.join(os.getcwd(), static_folder)
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

    def set_db_client(self, db_client: SoflyDbClient):
        self._db_client = db_client
        return self

    def set_jwt_service(self, jwt_service: JWTService):
        self._jwt_service = jwt_service
        return self

    def set_ai_model(self, ai_model):
        self.ai_model = ai_model
        return self

    def build(self) -> SoflyServer | None:

        if self._host is None:
            logger.critical("You must provide a host - host not provided")
            return None

        if self._db_client is None:
            logger.critical("You must provide a database client - db_client not provided")
            return None
        if self._jwt_service is None:
            logger.critical("You must provide a JWT service - jwt_service not provided")
            return None

        if self.ai_model is None:
            logger.critical("You must provide an AI model - ai_model not provided")
            return None

        return SoflyServer(
            host=self._host,
            port=self._port,
            ai_model=self.ai_model,
            jwt_service=self._jwt_service,
            db_client=self._db_client,
            static_folder_path=self._static_folder,
            template_folder=self._template_folder,
            is_debug=self._is_debug,
            should_create_public_dir=self._should_create_public_dir
        )

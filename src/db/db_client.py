import aiomysql
from loguru import logger

from src.config import DatabaseConfig
from src.db.user_sofly_service import UserSoflyService

class SoflyDbClient:
    """
    A class to interact with the database using a connection pool.
    """
    def __init__(self, config: DatabaseConfig):
        """
        Initialize the database client with a connection pool.

        Args:
            config (SoflyConfig.DatabaseConfig): The database configuration object.
        """
        self.config = config
        self.pool = None
        self.user_service = None

    async def init_db_client(self) -> bool:
        """
        Initialize the database client.
        This method is called after the server is initialized.
        """
        logger.info("Establishing connection with database...")
        await self.connect()
        self.init_all_services()
        logger.info("Running post init check...")
        return self.post_init_check()

    def init_all_services(self):
        """
        Initialize all services that depend on the database connection.
        This method should be overridden in subclasses to initialize specific services.
        """
        self.user_service = UserSoflyService(self)

    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(
                user=self.config.username,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port,
                db=self.config.db_name,
            )
            logger.success("Database connection established.")
        except ConnectionRefusedError as conn_ref:
            logger.critical("Connection refused. Possible cause is wrong IP or PORT, please check the configuration file.")

    def post_init_check(self):
        if self.pool is None:
            logger.critical("Database connection pool is not initialized. Exiting")
            return False
        else:
            logger.success("All post init checks passed.")
            return True

    async def fetch(self, query: str, *args):
        """Execute a query and return the results."""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        """Execute a query without returning results."""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()

import asyncpg
from loguru import logger

from src.config import DatabaseConfig

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

    async def init_db_client(self) -> bool:
        """
        Initialize the database client.
        This method is called after the server is initialized.
        """
        logger.info("Establishing connection with database...")
        await self.connect()
        logger.info("Running post init check...")
        return self.post_init_check()

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=self.config.username,
                password=self.config.password,
                database=self.config.database,
                host=self.config.host,
                port=self.config.port,
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

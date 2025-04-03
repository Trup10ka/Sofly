import pymysql
from loguru import logger
from dbutils.pooled_db import PooledDB

from src.config import DatabaseConfig
from src.db.insurance_abc_service import InsuranceService
from src.db.insurance_sofly_service import InsuranceSoflyService
from src.db.user_sofly_service import UserSoflyService
from src.db.user_abc_service import UserService

class SoflyDbClient:
    """
    A class to interact with the database using a connection pool.
    """
    def __init__(self, config: DatabaseConfig):
        """
        Initialize the database client with a connection pool.

        Args:
            :param config: (SoflyConfig.DatabaseConfig): The database configuration object.
        """
        self.config = config
        self.pool = None
        self.user_service: UserService | None = None
        self.insurance_service: InsuranceService | None = None

    def init_db_client(self) -> bool:
        """
        Initialize the database client.
        This method is called after the server is initialized.
        """
        logger.info("Establishing connection with database...")
        self.connect()
        self.init_all_services()
        logger.info("Running post init check...")
        return self.post_init_check()

    def init_all_services(self):
        """
        Initialize all services that depend on the database connection.
        This method should be overridden in subclasses to initialize specific services.
        """
        self.user_service = UserSoflyService(self)
        self.insurance_service = InsuranceSoflyService(self)

    def connect(self):
        try:
            self.pool = PooledDB(
                creator=pymysql,
                mincached=1,
                maxcached=5,
                blocking=True,
                host=self.config.host,
                user=self.config.username,
                password=self.config.password,
                port=self.config.port,
                database=self.config.db_name,
                autocommit=False,
                cursorclass=pymysql.cursors.DictCursor  # Return results as dictionaries
            )
            logger.success("Database connection established.")
        except pymysql.MySQLError as e:
            logger.critical(f"Connection refused. Error: {e}")

    def post_init_check(self):
        if self.pool is None:
            logger.critical("Database connection pool is not initialized. Exiting")
            return False
        else:
            logger.success("All post init checks passed.")
            return True

    def fetch(self, query, *args):
        """Execute a query and return the results."""
        connection = self.pool.connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchall()
        finally:
            connection.close()

    def execute(self, query, *args):
        """Execute a query without returning results."""
        connection = self.pool.connection()
        try:
            with connection.cursor() as cursor:
                result = cursor.execute(query, args)
                connection.commit()
                return result
        finally:
            connection.close()

    def close(self):
        """Close the database connection pool."""
        if self.pool:
            self.pool.close()

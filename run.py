import asyncio

from loguru import logger

from src.config.pyhocon_config_loader import PyhoconConfigLoader
from src.db.db_client import SoflyDbClient
from src.security import JWTService
from src.sofly_server import SoflyServer

async def main():

    config = PyhoconConfigLoader("config.conf").load_config()


    if config == -1:
        logger.critical("Failed to load configuration file, exiting...")
        return
    elif config == 1:
        logger.info("Exiting program.")
        return

    db_client = SoflyDbClient(config.database)
    if not await db_client.init_db_client():
        return

    jwt_service = JWTService(config.jwt.secret_key)

    server = (SoflyServer.builder()
              .set_host(config.server.host)
              .set_port(config.server.port)
              .build())

    if server is None:
        raise RuntimeError("SoflyServer not initialized, fatal error, exiting...")

    server.init()
    server.run()

if __name__ == '__main__':
    asyncio.run(main())
import datetime
import pickle as pkl
import sys
from loguru import logger

from src.config import SoflyConfig
from src.config.pyhocon_config_loader import PyhoconConfigLoader
from src.db.db_client import SoflyDbClient
from src.security import JWTService
from src.sofly_server import SoflyServer

def init_db() -> tuple[SoflyConfig | None, SoflyDbClient | None]:
    """
    Initialize the database client and return the config and db client.
    """
    config = PyhoconConfigLoader("config.conf").load_config()

    if config == -1:
        logger.critical("Failed to load configuration file, exiting...")
        return None, None
    elif config == 1:
        logger.info("Exiting program.")
        return None, None

    db_client = SoflyDbClient(config.database)
    if not db_client.init_db_client():
        return None, None

    return config, db_client

def load_ai(file_name: str):
    try:
        with open(f".models/{file_name}", "rb") as model_file:
            return pkl.load(model_file)
    except FileNotFoundError:
        logger.error("Model file not found. Please train the model first and save it to .model folder.")
        exit(1)

def main(ai_model, sofly_config: SoflyConfig, sofly_db_client: SoflyDbClient):

    jwt_service = JWTService(sofly_config.jwt_secret)

    generated_template_token = jwt_service.generate_jwt(
        {"username": "jirkakral", "password": "template_password"},
    )

    logger.debug(f"Generated template token: {generated_template_token}")

    server = (SoflyServer.builder()
              .set_host(sofly_config.server.host)
              .set_port(sofly_config.server.port)
              .set_jwt_service(jwt_service)
              .set_db_client(sofly_db_client)
              .set_debug(True)
              .set_ai_model(ai_model)
              .build())

    if server is None:
        raise RuntimeError("SoflyServer not initialized, fatal error, exiting...")

    server.init()
    server.run()


if __name__ == '__main__':

    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS zz}</green> | <level>{level: <8}</level> | <yellow>Line {line: >4} ({file}):</yellow> <b>{message}</b>"
    logger.add(f"sofly-{datetime.datetime.now().strftime('%Y-%m-%d')}.log", level="INFO", format=log_format, colorize=False, backtrace=True, diagnose=True)

    if len(sys.argv) < 2:
        logger.critical("No argument provided for AI model, exiting...")
        exit(1)
    arg = sys.argv[1]
    logger.info(f"Argument received: {arg}")

    loaded_model = load_ai(f'{arg}.llm.pkl')

    s_config, s_db_client = init_db()
    if s_config is None or s_db_client is None:
        logger.critical("Failed to initialize database client, exiting...")
        exit(1)

    main(loaded_model, s_config, s_db_client)

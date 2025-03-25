from flask import send_from_directory, Flask
from loguru import logger


def init_endpoints(app: Flask):
    @app.route('/')
    def serve_index():
        logger.info("Request to '/' from origin: ")
        return send_from_directory('..', 'index.html')


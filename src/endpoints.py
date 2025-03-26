from flask import send_from_directory, Flask, Blueprint
from loguru import logger


def init_endpoints(app: Flask):
    api_endpoint = Blueprint('api_endpoint', __name__, url_prefix='/api')

    init_api_endpoints(api_endpoint)

    init_html_endpoints(app)

    register_all_blueprints(app, api_endpoint)


def init_api_endpoints(api_blueprint: Blueprint):
    @api_blueprint.route('/sofas')
    def serve_sofas():
        logger.info("Request to '/api/sofas' from origin: ")
        return send_from_directory('..', 'sofas.json')

    @api_blueprint.route('/tables')
    def serve_tables():
        logger.info("Request to '/api/tables' from origin: ")
        return send_from_directory('..', 'tables.json')


def init_html_endpoints(app: Flask):
    @app.route('/')
    def serve_index():
        logger.info("Request to '/' from origin: ")
        return send_from_directory('..', 'index.html')

    @app.route('/sofas')
    def serve_sofas():
        logger.info("Request to '/sofas' from origin: ")
        return send_from_directory('..', 'sofas.html')

    @app.route('/tables')
    def serve_tables():
        logger.info("Request to '/tables' from origin: ")
        return send_from_directory('..', 'tables.html')


def register_all_blueprints(app: Flask, *blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

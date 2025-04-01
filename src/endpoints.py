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

    HTML_DIR = '../sites'

    @app.route('/')
    def serve_index():
        logger.info("Request to '/' from origin: ")
        return send_from_directory(HTML_DIR, 'index.html')

    @app.route('/dashboard')
    def serve_sofas():
        logger.info("Request to '/sofas' from origin: ")
        return send_from_directory(HTML_DIR, 'dashboard.html')

    @app.route('/insurance')
    def serve_tables():
        logger.info("Request to '/tables' from origin: ")
        return send_from_directory(HTML_DIR, 'insurance.html')

    @app.route('/insured-event')
    def serve_insured_event():
        logger.info("Request to '/insured-event' from origin: ")
        return send_from_directory(HTML_DIR, 'insured-event.html')


def register_all_blueprints(app: Flask, *blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

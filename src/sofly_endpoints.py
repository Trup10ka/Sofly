import src.sofly_server as sofly

from flask import Flask, Blueprint
from src.endpoints import init_html_endpoints, init_api_endpoints



def init_endpoints(app: 'sofly.SoflyServer'):
    api_endpoint = Blueprint('api_endpoint', __name__, url_prefix='/api')

    init_api_endpoints(api_endpoint, app.jwt_service, app.db_client.user_service)

    init_html_endpoints(app.flask_app)

    register_all_blueprints(app.flask_app, api_endpoint)



def register_all_blueprints(app: Flask, *blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

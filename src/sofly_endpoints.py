from flask import Flask, Blueprint
from endpoints import init_html_endpoints, init_api_endpoints


def init_endpoints(app: Flask):
    api_endpoint = Blueprint('api_endpoint', __name__, url_prefix='/api')

    init_api_endpoints(api_endpoint)

    init_html_endpoints(app)

    register_all_blueprints(app, api_endpoint)



def register_all_blueprints(app: Flask, *blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

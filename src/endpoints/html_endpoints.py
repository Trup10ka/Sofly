from flask import Flask, send_from_directory, request, redirect
from loguru import logger

from src.security import JWTService


def init_html_endpoints(app: Flask, jwt_service: JWTService):

    HTML_DIR = '../sites'

    @app.route('/')
    def serve_index():
        logger.info("Request to '/' from origin: ")
        return send_from_directory(HTML_DIR, 'index.html')

    @app.route('/register')
    def server_register():
        logger.info("Request to '/register' from origin: ")
        return send_from_directory(HTML_DIR, 'register.html')

    @app.route('/dashboard')
    def serve_sofas():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info("Request to '/dashboard' from origin: ")
        return send_from_directory(HTML_DIR, 'dashboard.html')

    @app.route('/insurance')
    def serve_tables():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info("Request to '/insured-event' from origin: ")
        return send_from_directory(HTML_DIR, 'insurance.html')

    @app.route('/insured-event')
    def serve_insured_event():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info("Request to '/insured-event' from origin: ")
        return send_from_directory(HTML_DIR, 'insured-event.html')

def is_authenticated(jwt_service: JWTService) -> bool:
    """
    Check if the user is authenticated.
    :param jwt_service:
    :return: True if the user is authenticated, False otherwise.
    """
    token = request.cookies.get('SOFLY_TOKEN')
    try:
        data, status_code = jwt_service.verify_jwt(token)
        return status_code == 200
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return False
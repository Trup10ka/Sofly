from flask import Flask, send_from_directory, request, redirect
from loguru import logger

from src.endpoints.util import is_authenticated
from src.security import JWTService


def init_html_endpoints(app: Flask, jwt_service: JWTService):

    HTML_DIR = '../sites'

    @app.route('/')
    def serve_index():
        logger.info(f"Request to '/' from origin: {request.remote_addr}")
        return send_from_directory(HTML_DIR, 'index.html')

    @app.route('/register')
    def server_register():
        logger.info(f"Request to '/register' from origin: {request.remote_addr}")
        return send_from_directory(HTML_DIR, 'register.html')

    @app.route('/dashboard')
    def serve_sofas():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info(f"Request to '/dashboard' from origin: {request.remote_addr}")
        return send_from_directory(HTML_DIR, 'dashboard.html')

    @app.route('/insurance')
    def serve_tables():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info(f"Request to '/insured-event' from origin: {request.remote_addr}")
        return send_from_directory(HTML_DIR, 'insurance.html')

    @app.route('/report')
    def serve_insured_event():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        logger.info(f"Request to '/insured-event' from remote address: {request.remote_addr}")
        return send_from_directory(HTML_DIR, 'report-event.html')

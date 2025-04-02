from flask import Flask, send_from_directory
from loguru import logger


def init_html_endpoints(app: Flask):

    HTML_DIR = '../sites'

    @app.route('/')
    def serve_index():
        logger.info("Request to '/' from origin: ")
        return send_from_directory(HTML_DIR, 'index.html')

    @app.route('/dashboard')
    def serve_sofas():
        logger.info("Request to '/dashboard' from origin: ")
        return send_from_directory(HTML_DIR, 'dashboard.html')

    @app.route('/insurance')
    def serve_tables():
        logger.info("Request to '/tables' from origin: ")
        return send_from_directory(HTML_DIR, 'insurance.html')

    @app.route('/insured-event')
    def serve_insured_event():
        logger.info("Request to '/insured-event' from origin: ")
        return send_from_directory(HTML_DIR, 'insured-event.html')
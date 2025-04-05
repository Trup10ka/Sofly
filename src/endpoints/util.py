from flask import request
from loguru import logger

from src.security import JWTService


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
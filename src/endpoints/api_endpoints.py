from flask import Blueprint, send_from_directory

from src.db.user_abc_service import UserService
from src.endpoints.login_api_endpoints import init_auth_endpoints
from src.security import JWTService


def init_api_endpoints(api_blueprint: Blueprint, jwt_service: JWTService, user_service: UserService):

    init_auth_endpoints(api_blueprint, user_service, jwt_service)



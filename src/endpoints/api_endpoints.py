from flask import Blueprint, send_from_directory

from src.db import SoflyDbClient
from src.endpoints.auth_api_endpoints import init_auth_endpoints
from src.endpoints.dashboard_endpoints import init_api_dashboard_endpoints
from src.security import JWTService


def init_api_endpoints(api_blueprint: Blueprint, jwt_service: JWTService, db_client: SoflyDbClient):

    init_auth_endpoints(api_blueprint, db_client.user_service, jwt_service)

    init_api_dashboard_endpoints(db_client.insurance_service, api_blueprint, jwt_service)

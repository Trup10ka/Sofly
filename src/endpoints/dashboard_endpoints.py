import asyncio

from flask import Blueprint, request

from src.db.insurance_sofly_service import InsuranceSoflyService
from src.security import JWTService


def init_api_dashboard_endpoints(insurance_service: InsuranceSoflyService, blueprint: Blueprint, jwt_service: JWTService):

    @blueprint.route('/all-my-insurances', methods=['GET'])
    def get_all_my_insurances():
        token_cookie = request.cookies.get('SOFLY_TOKEN')

        if not token_cookie:
            return {'error': 'Token not found in cookies'}, 401

        decoded_token, status_code = jwt_service.verify_jwt(token_cookie)

        if status_code != 200:
            return decoded_token, status_code

        user_all_insurances = insurance_service.get_all_insurances_by_user(decoded_token['username'])

        if not user_all_insurances:
            return {'error': 'No insurances found for this user'}, 404

        return [insurance.to_dict() for insurance in user_all_insurances], 200



    @blueprint.route('/all-my-insurances/<insurance_id>', methods=['GET'])
    def et_insurance_by_id(insurance_id: str):
        token_cookie = request.cookies.get('SOFLY_TOKEN')

        if not token_cookie:
            return {'error': 'Token not found in cookies'}, 401

        decoded_token, status_code = jwt_service.verify_jwt(token_cookie)

        if status_code != 200:
            return decoded_token, status_code

        # TODO: WRONG
        user_insurance = insurance_service.get_insurance_by_id(decoded_token['insurance_id'])

        if not user_insurance:
            return {'error': 'Insurance not found'}, 404

        return user_insurance.to_dict(), 200
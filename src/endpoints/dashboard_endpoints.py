import asyncio
from datetime import datetime

from flask import Blueprint, request, redirect

from src.data import InsuranceDTO
from src.db.insurance_sofly_service import InsuranceSoflyService
from src.endpoints.util import is_authenticated
from src.security import JWTService


def init_api_dashboard_endpoints(insurance_service: InsuranceSoflyService, blueprint: Blueprint, jwt_service: JWTService):

    @blueprint.route('/all-my-insurances', methods=['GET'])
    def get_all_my_insurances():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        token_cookie = request.cookies.get('SOFLY_TOKEN')

        decoded_token, status_code = jwt_service.verify_jwt(token_cookie)

        user_all_insurances = insurance_service.get_all_insurances_by_user(decoded_token['username'])

        if not user_all_insurances:
            return {'error': 'No insurances found for this user'}, 404

        return [insurance.to_dict() for insurance in user_all_insurances], 200



    @blueprint.route('/all-my-insurances/<insurance_id>', methods=['GET'])
    def get_insurance_by_id(insurance_id: str):
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        token_cookie = request.cookies.get('SOFLY_TOKEN')

        decoded_token, status_code = jwt_service.verify_jwt(token_cookie)

        # TODO: WRONG
        user_insurance = insurance_service.get_insurance_by_id(decoded_token['insurance_id'])

        if not user_insurance:
            return {'error': 'Insurance not found'}, 404

        return user_insurance.to_dict(), 200

    @blueprint.route('/create-insurance', methods=['POST'])
    def create_insurance():
        if not is_authenticated(jwt_service):
            return redirect("/", code=302)

        token_cookie = request.cookies.get('SOFLY_TOKEN')

        decoded_token, status_code = jwt_service.verify_jwt(token_cookie)

        insurance_data = request.json

        if not insurance_data:
            return {'error': 'No data provided'}, 400

        insurance_data['user_id'] = decoded_token['username']

        cost = { "basic": 1450.00, "advanced": 3450.00, "full": 6200.00 }.get(insurance_data['insurance_type'], 0)

        if cost == 0:
            return {'error': 'Invalid insurance type'}, 400

        insurance_dto = InsuranceDTO(
            for_username=decoded_token['username'],
            insurance_type=insurance_data['insurance_type'],
            start_date=datetime.now().strftime('%Y-%m-%d'),
            cost_per_month=cost,
            end_date=insurance_data.get('end_date', None),
            status="pending",
        )

        new_insurance = insurance_service.create_insurance(insurance_dto)

        if not new_insurance:
            return {'error': 'Insurance creation failed'}, 500

        return "Successful", 201
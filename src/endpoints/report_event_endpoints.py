import numpy as np
from flask import Blueprint, request

from src.endpoints.util import is_authenticated
from src.security import JWTService


def init_api_report_event_endpoints(blueprint: Blueprint, jwt_service: JWTService, ai_model):

    @blueprint.route('/report-event', methods=['POST'])
    def report_event():
        if not is_authenticated(jwt_service):
            return {'error': 'Unauthorized'}, 401

        event_data = request.json

        furniture_set: list[dict] = event_data.get('furniture_set')
        insurance_type: str = event_data.get('insurance_type')

        if not event_data or not furniture_set or not insurance_type :
            return {'error': 'Invalid data'}, 400

        furniture_set_2d = []

        for furniture in furniture_set:
            furniture_values = list(furniture.values())
            furniture_set_2d.append(furniture_values)

        furniture_set_2d = np.array(furniture_set_2d)
        result = ai_model.predict(furniture_set_2d)

        result_sum = sum(float(x) for x in result)

        if insurance_type == 'basic':
            result_sum *= 3000 * 0.4
        elif insurance_type == 'advanced':
            result_sum *= 3000 * 0.8
        elif insurance_type == 'full':
            result_sum *= 3000 * 1.4

        return {'result': result_sum}, 200
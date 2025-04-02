from src.db.insurance_abc_service import InsuranceService


class InsuranceSoflyService(InsuranceService):

    async def create_insurance(self, insurance_data: dict):
        pass

    async def get_insurance_by_id(self, insurance_id: str):
        pass

    async def get_insurance_by_sofly_id(self, insurance_name: str):
        pass

    async def change_state_of_insurance(self, insurance_id: str, state: str):
        pass

    async def get_all_insurances_by_user(self, user_id: str):
        pass

    async def get_all_insurances(self):
        pass
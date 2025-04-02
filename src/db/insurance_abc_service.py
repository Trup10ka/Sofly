from abc import ABC, abstractmethod

import src.db.db_client as db_c

class InsuranceService(ABC):

    def __init__(self, db_client: 'db_c.SoflyDbClient'):
        self.db_client = db_client

    @abstractmethod
    async def create_insurance(self, insurance_data: dict):
        pass


    @abstractmethod
    async def get_insurance_by_id(self, insurance_id: str):
        pass

    @abstractmethod
    async def get_insurance_by_sofly_id(self, insurance_name: str):
        pass

    @abstractmethod
    async def change_state_of_insurance(self, insurance_id: str, state: str):
        pass

    @abstractmethod
    async def get_all_insurances_by_user(self, user_id: str):
        pass

    @abstractmethod
    async def get_all_insurances(self):
        pass

from abc import ABC, abstractmethod

from src.data import Insurance, InsuranceDTO

import src.db.db_client as db_c


class InsuranceService(ABC):

    def __init__(self, db_client: 'db_c.SoflyDbClient'):
        self.db_client = db_client

    @abstractmethod
    async def create_insurance(self, insurance_data: InsuranceDTO) -> bool:
        pass

    @abstractmethod
    async def get_insurance_by_id(self, insurance_id: str) -> Insurance | None:
        pass

    @abstractmethod
    async def get_insurance_by_sofly_id(self, insurance_name: str) -> Insurance | None:
        pass

    @abstractmethod
    async def change_state_of_insurance(self, insurance_id: str, state: str) -> Insurance | None:
        pass

    @abstractmethod
    async def get_all_insurances_by_user(self, user_id: str) -> list[Insurance]:
        pass

    @abstractmethod
    async def get_all_insurances(self) -> list[Insurance]:
        pass

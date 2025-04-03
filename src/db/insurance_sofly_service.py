from src.data import InsuranceDTO, Insurance
from src.db.insurance_abc_service import InsuranceService

import src.db.db_client as db_c


def return_all_insurances(result) -> list[Insurance]:
    insurances = []
    for insurance in result:
        insurances.append(Insurance(
            db_id=insurance['id'],
            user_id=insurance['user_id'],
            insurance_id=insurance['insurance_id'],
            insurance_type=insurance['type_of_insurance'],
            cost_per_month=insurance['cost_per_month'],
            status=insurance['status'],
            start_date=insurance['start_date'],
            end_date=insurance['end_date']
        ))

    return insurances

class InsuranceSoflyService(InsuranceService):

    def __init__(self, db_client: 'db_c.SoflyDbClient'):
        super().__init__(db_client)

    async def create_insurance(self, insurance_data: InsuranceDTO) -> bool:
        type_of_insurance_id = await self.db_client.fetch(
            "SELECT id FROM type_of_insurance WHERE name = $s",
            insurance_data.insurance_type
        )

        if not type_of_insurance_id:
            return False

        user_id = await self.db_client.fetch(
            "SELECT id FROM users WHERE username = %s",
            insurance_data.for_username
        )
        if not user_id:
            return False

        result = await self.db_client.execute(
            "INSERT INTO insurance (user_id, type_of_insurance, cost_per_month, status, start_date, end_date) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            user_id,
            type_of_insurance_id,
            insurance_data.cost_per_month,
            insurance_data.status,
            insurance_data.start_date,
            insurance_data.end_date
        )

        return result == 1


    async def get_insurance_by_id(self, insurance_id: str) -> Insurance | None:
        result = await self.db_client.fetch(
            "SELECT * FROM insurance WHERE id = %s",
            insurance_id
        )

        if result:
            insurance = result[0]
            return Insurance(
                db_id=insurance['id'],
                user_id=insurance['user_id'],
                insurance_id=insurance['insurance_id'],
                insurance_type=insurance['type_of_insurance'],
                cost_per_month=insurance['cost_per_month'],
                status=insurance['status'],
                start_date=insurance['start_date'],
                end_date=insurance['end_date']
            )
        return None

    async def get_insurance_by_sofly_id(self, sofly_uuid: str) -> Insurance | None:
        result = await self.db_client.fetch(
            "SELECT * FROM insurance WHERE sofly_uuid = %s",
            sofly_uuid
        )

        if result:
            insurance = result[0]
            return Insurance(
                db_id=insurance['id'],
                user_id=insurance['user_id'],
                insurance_id=insurance['insurance_id'],
                insurance_type=insurance['type_of_insurance'],
                cost_per_month=insurance['cost_per_month'],
                status=insurance['status'],
                start_date=insurance['start_date'],
                end_date=insurance['end_date']
            )

    async def change_state_of_insurance(self, insurance_id: str, state: str) -> Insurance | None:
        insurance_db_id = await self.db_client.fetch(
            "SELECT id FROM insurance WHERE sofly_uuid = %s",
            insurance_id
        )

        result = await self.db_client.fetch(
            "UPDATE insurance SET status = %s WHERE id = %s",
            state,
            insurance_db_id
        )

        if result.rowcount == 1:
            return Insurance(
                db_id=insurance_db_id,
                insurance_id=insurance_id,
                user_id=result[0]['user_id'],
                insurance_type=result[0]['type_of_insurance'],
                cost_per_month=result[0]['cost_per_month'],
                status=result[0]['status'],
                start_date=result[0]['start_date'],
                end_date=result[0]['end_date']
            )

    async def get_all_insurances_by_user(self, username: str) -> list[Insurance]:
        result = await self.db_client.fetch(
            "SELECT * FROM insurance WHERE user_id = (SELECT id FROM users WHERE username = %s)",
            username
        )

        return return_all_insurances(result)

    async def get_all_insurances(self) -> list[Insurance]:
        result = await self.db_client.fetch(
            "SELECT * FROM insurance"
        )

        return return_all_insurances(result)

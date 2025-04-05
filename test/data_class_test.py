import unittest

from unittest.mock import MagicMock

from src.config.pyhocon_config_loader import PyhoconConfigLoader
from src.db import SoflyDbClient
from src.db.insurance_sofly_service import InsuranceSoflyService

from src.data import Insurance, InsuranceDTO


class DataClassTest(unittest.TestCase):

    def test_insurance_data_class_to_dict(self):
        insurance = Insurance(
            db_id=1,
            user_id=123,
            insurance_id="INS123",
            insurance_type="health",
            cost_per_month=99.99,
            status="active",
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
        expected_dict = {
            "db_id": 1,
            "user_id": 123,
            "insurance_id": "INS123",
            "insurance_type": "health",
            "cost_per_month": 99.99,
            "status": "active",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
        self.assertEqual(insurance.to_dict(), expected_dict)

    def test_correct_insurance_object_init(self):
        insurance = Insurance(db_id=1, user_id=100, insurance_id="INS001", insurance_type="home",
                              cost_per_month=50.0, status="active")
        self.assertEqual(insurance.db_id, 1)

    def test_create_insurance(self):
        config = PyhoconConfigLoader("config.conf").load_config()

        if config is None:
            raise ValueError("Configuration file not found or invalid.")
        if config.database is None:
            raise ValueError("Database configuration not found in the configuration file.")

        db_client = SoflyDbClient(config.database)
        db_client.init_db_client()

        db_client.insurance_service.create_insurance(
            InsuranceDTO(
                for_username="friedl",
                insurance_type="full",
                cost_per_month=99.99,
                status="active",
                start_date="2023-01-01",
                end_date="2023-12-31"
            )
        )

        insurance = db_client.insurance_service.get_all_insurances_by_user("friedl")
        self.assertIsNotNone(insurance)

if __name__ == '__main__':
    unittest.main()

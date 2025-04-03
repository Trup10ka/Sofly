from typing import Literal

class Insurance:

    def __init__(self, db_id: int, user_id: int, insurance_id: str, insurance_type: str, cost_per_month: float,
                 status: Literal['active', 'inactive', 'pending'],
                 start_date: str = None, end_date: str = None):
        self.db_id = db_id
        self.user_id = user_id
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type
        self.cost_per_month = cost_per_month
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return (f"InsuranceDTO(db_id={self.db_id}, user_id={self.user_id}, "
                f"insurance_id={self.insurance_id}, insurance_type={self.insurance_type}, "
                f"cost_per_month={self.cost_per_month}, status={self.status}, "
                f"start_date={self.start_date}, end_date={self.end_date})")

    def to_dict(self):
        return {
            "db_id": self.db_id,
            "user_id": self.user_id,
            "insurance_id": self.insurance_id,
            "insurance_type": self.insurance_type,
            "cost_per_month": self.cost_per_month,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
from typing import Literal

class InsuranceDTO:

    def __init__(self, user_id: int, insurance_id: int, insurance_type: str, cost_per_month: float,
                 status: Literal['active', 'inactive', 'pending'],
                 start_date: str = None, end_date: str = None, ):
        self.user_id = user_id
        self.insurance_id = insurance_id
        self.insurance_type = insurance_type
        self.cost_per_month = cost_per_month
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return (f"InsuranceDTO(user_id={self.user_id}, insurance_id={self.insurance_id}, "
                f"insurance_type={self.insurance_type}, cost_per_month={self.cost_per_month},"
                f" status={self.status}, start_date={self.start_date}, end_date={self.end_date})")

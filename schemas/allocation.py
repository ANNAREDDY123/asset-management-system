from pydantic import BaseModel
from datetime import date


class AllocationCreate(BaseModel):

    asset_id: int

    employee_id: int

    assigned_date: date

    return_date: date | None = None

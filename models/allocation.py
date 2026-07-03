from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base


class Allocation(Base):
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    employee_id = Column(Integer, ForeignKey("users.id"))
    assigned_date = Column(Date)
    return_date = Column(Date, nullable=True)
    allocation_status = Column(String, default="Assigned")

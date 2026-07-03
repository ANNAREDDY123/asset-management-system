from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    asset_name = Column(String)
    asset_type = Column(String)
    asset_tag = Column(String, unique=True)
    purchase_date = Column(Date)
    status = Column(String)
    is_active = Column(Boolean, default=True)

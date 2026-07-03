from pydantic import BaseModel, Field
from datetime import date


class AssetCreate(BaseModel):

    asset_name: str = Field(..., min_length=2)

    asset_type: str

    asset_tag: str = Field(..., min_length=3)

    purchase_date: date

    status: str

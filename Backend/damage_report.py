from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from decimal import Decimal

class DamageReport(BaseModel):
    tenant_id: str = Field(..., example="T1001")
    flat_number: str = Field(..., example="A-101")
    description: str = Field(..., example="Broken bathroom tiles")
    severity: str = Field(..., example="moderate")  # minor | moderate | severe
    estimated_cost: Decimal = Field(..., example=1500.00)
    photo_url: Optional[HttpUrl] = Field(None, example="https://s3.amazonaws.com/bucket/damage/photo.jpg")

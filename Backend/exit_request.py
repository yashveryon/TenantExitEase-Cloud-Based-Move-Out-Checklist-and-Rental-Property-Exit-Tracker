from pydantic import BaseModel, EmailStr, Field
from datetime import date

class ExitRequest(BaseModel):
    tenant_name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    flat_number: str = Field(..., example="A-101")
    exit_date: date = Field(..., example="2025-07-01")
    reason: str = Field(..., example="Relocation due to job change")

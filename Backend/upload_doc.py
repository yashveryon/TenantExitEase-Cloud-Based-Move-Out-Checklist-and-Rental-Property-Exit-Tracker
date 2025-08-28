from pydantic import BaseModel, Field

class DocumentUpload(BaseModel):
    filename: str = Field(..., example="agreement.pdf")
    filetype: str = Field(..., example="application/pdf")
    content: bytes  # Will be handled as `UploadFile` in route

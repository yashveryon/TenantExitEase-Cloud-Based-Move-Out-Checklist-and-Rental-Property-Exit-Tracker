from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.s3_service import upload_file_to_s3

router = APIRouter(prefix="/upload", tags=["File Upload"])

@router.post("/document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the 'tenant_docs' folder in the configured S3 bucket.
    """
    try:
        s3_url = upload_file_to_s3(file, folder="tenant_docs")
        return {
            "message": "File uploaded successfully",
            "file_url": s3_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

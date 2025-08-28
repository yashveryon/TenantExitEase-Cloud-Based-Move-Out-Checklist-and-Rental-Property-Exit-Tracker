import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from fastapi import UploadFile
from app.config.settings import settings
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.clean_region
)

def upload_file_to_s3(file: UploadFile, folder: str = "uploads") -> str:
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
        s3_client.upload_fileobj(file.file, settings.S3_BUCKET_NAME, unique_filename)
        s3_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
        return s3_url
    except (BotoCoreError, NoCredentialsError) as e:
        raise Exception(f"S3 upload failed: {e}")

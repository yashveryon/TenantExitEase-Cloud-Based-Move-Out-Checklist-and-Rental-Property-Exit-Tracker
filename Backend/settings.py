from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    # AWS credentials
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    # AWS region (with default fallback)
    AWS_REGION: str = "us-east-1"

    # AWS services
    S3_BUCKET_NAME: str
    SES_EMAIL: EmailStr  # Validates format like example@example.com

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def clean_region(self) -> str:
        """Sanitize AWS region name by stripping extra spaces or comments"""
        return self.AWS_REGION.strip().split()[0]  # gets 'us-east-1' from 'us-east-1 # comment'


# Singleton instance for reuse across the app
settings = Settings()

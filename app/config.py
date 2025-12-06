from pydantic_settings import BaseSettings
from pydantic import Field
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")

load_dotenv(env_path)


class Settings(BaseSettings):
    # Main database
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")
    database_url: str = Field(alias="DATABASE_URL")

    # Test database
    postgres_test_user: str = Field(alias="POSTGRES_TEST_USER")
    postgres_test_password: str = Field(alias="POSTGRES_TEST_PASSWORD")
    postgres_test_db: str = Field(alias="POSTGRES_TEST_DB")

    # JWT auth
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # SMTP
    smtp_host: str = Field(alias="SMTP_HOST", default="localhost")
    smtp_port: int = Field(alias="SMTP_PORT", default=1025)
    smtp_user: str = Field(alias="SMTP_USER", default="")
    smtp_password: str = Field(alias="SMTP_PASSWORD", default="")
    mail_from: str = Field(alias="MAIL_FROM", default="noreply@contacts.local")

    app_url: str = Field(alias="APP_URL")

    # Cloudinary
    cloudinary_name: str = Field(alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(alias="CLOUDINARY_API_SECRET")

    model_config = {
        "env_file": ".env",     # ← только .env — ЭТО КОНЕЧНОЕ ПРАВИЛЬНОЕ РЕШЕНИЕ
        "extra": "ignore",
        "populate_by_name": True,
    }

    redis_url: str = "redis://localhost:6379"


settings = Settings()

from pydantic_settings import BaseSettings
from pydantic import Field



class Settings(BaseSettings):
    # Database
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # JWT auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # SMTP
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    mail_from: str

    app_url: str

    # Cloudinary
    cloudinary_name: str = Field(alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(alias="CLOUDINARY_API_SECRET")

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "populate_by_name": True,
    }

settings = Settings()


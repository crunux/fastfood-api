import os
import secrets
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    PROJECT_NAME: str = f"Store API - {
        os.getenv('ENV', 'development').capitalize()}"
    DESCRIPTION: str = "This is a store API"
    ENV: Literal["development", "production"] = "development"
    VERSION: str = "0.1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    DATABASE_URL: str = "postgresql://store_owner:guw1xtJ7hIeo@ep-lingering-tooth-a5zaa2z5.us-east-2.aws.neon.tech/store"
    # DATABASE_URL: str = "postgresql://store_owner:guw1xtJ7hIeo@ep-lingering-tooth-a5zaa2z5.us-east-2.aws.neon.tech/store?sslmode=require"
    API_V1_STR: str = "/api/v1"
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "admin"
    ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5000",
        "*"
    ]
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120


class Config:
    case_sensitive = True


settings = Settings()


class TestConfig(Settings):
    class Config:
        case_sensitive = True


test_settings = TestConfig()


# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbG9uc29kQGV4YW1wbGUuY29tIiwiZXhwIjoxNzI1NzY3NDUzfQ.yQ6ED9BCmeunvNuV3_A4yzcazcKlH2GR_EcsTVp8Wmg",
#   "token_type": "Bearer",
#   "user": {
#     "name": "Alonso Doe",
#     "email": "alonsod@example.com",
#     "date_of_birth": "1995-09-01",
#     "is_active": true,
#     "is_admin": true,
#     "personalID": "987654321",
#     "id": "1ab74c30-00c0-4a11-a257-0a76d94f5362"
#   }
# }
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
    DATABASE_URL: str = "postgresql://root:Cross19950502@127.0.0.1:5432/fastfood"
    # DATABASE_URL: str = "postgresql://store_owner:guw1xtJ7hIeo@ep-lingering-tooth-a5zaa2z5.us-east-2.aws.neon.tech/store"
    # DATABASE_URL: str = "postgresql://store_owner:guw1xtJ7hIeo@ep-lingering-tooth-a5zaa2z5.us-east-2.aws.neon.tech/store?sslmode=require"
    API_V1_STR: str = "/api/v1"
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "admin"
    API_EMAIL: str = "joancruz0502@hotmail.com"
    ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:8100",
        "*"
    ]
    SECRET_KEY: str = "e13803a67359c67e64acfe5c943bc0d41edde0f8e5f4f6fb2839f3fe8460ab27"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    SERVER_HOST: str = "http://127.0.0.1:5000"
    


class Config:
    case_sensitive = True


settings = Settings()


class TestConfig(Settings):
    class Config:
        case_sensitive = True


test_settings = TestConfig()


# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZEBleGFtcGxlLmNvbSIsImV4cCI6MTcyNTgzMjgxMn0.FO3O3MtSGb5x2Dj6e2gwlCESB7jSvgRHNJej9FUJ71g",
#   "token_type": "Bearer",
#   "user": {
#     "name": "John Doe",
#     "email": "johnd@example.com",
#     "date_of_birth": "1990-01-01",
#     "is_active": true,
#     "is_admin": false,
#     "personalID": "123456789",
#     "id": "54ef0eb1-52be-46ef-ba8c-58c50286c6ed"
#   }
# }
#admin
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbG9uc29kQGV4YW1wbGUuY29tIiwiZXhwIjoxNzI1ODM2MzE3fQ.HVaNMW_2oOE37Aky_SKfoTU8MN9WsxTr8UOQLGjqArA",
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
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
import uuid


class UserBase(SQLModel):
    name: str
    email: str | None = Field(EmailStr, index=True)
    date_of_birth: str
    is_active: bool = True
    is_admin: bool = False
    personalID: str = ""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johnd@example.com",
                "password": "password",
                "date_of_birth": "1990-01-01",
                "is_active": True,
                "is_admin": False,
                "personalID": "123456789"
            }
        }


class LoginUser(SQLModel):
    email: str
    password: str


class User(UserBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field()


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    date_of_birth: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    personalId: str | None = None


class UserInDB(BaseModel):
    id: uuid.UUID
    name: str
    date_of_birth: str
    is_active: bool
    is_admin: bool
    personalID: str

    class Config:
        from_attributes = True
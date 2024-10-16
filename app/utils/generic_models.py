from fastapi import Form
from sqlmodel import Field, SQLModel
from pydantic import BaseModel
import uuid

from app.models.users import UserInDB


# class ProductCategory(SQLModel, table=True):
#     category_id: uuid.UUID | None = Field(
#         default_factory=uuid.uuid4, foreign_key="category.id", primary_key=True)
#     product_id: uuid.UUID | None = Field(
#         default_factory=uuid.uuid4, foreign_key="product.id", primary_key=True)


# class DetailsProductLink(SQLModel):
#     product_id: uuid.UUID = Field(foreign_key="product.id", primary_key=True)
#     details_order_id: uuid.UUID = Field(
#         foreign_key="details_order.id", primary_key=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserInDB


class OAuth2CustomPasswordRequestForm(BaseModel):
    email: str = Form()
    password: str = Form()


class Msg(BaseModel):
    msg: str

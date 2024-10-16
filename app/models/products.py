from decimal import Decimal
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from app.models.categories import Category, CategoryInDB

import uuid


class ProductBase(SQLModel):
    name: str
    description: str = ""
    price: Decimal
    tax: Decimal = 0.0
    active: bool = True
    image: str = ""
    category_id: uuid.UUID


class Product(ProductBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID | None = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    details_orders: list['DetailsOrder'] = Relationship( # type: ignore
        back_populates="product")
    image: str = Field(default="")


class ProductCreate(ProductBase):
    tax: Decimal | None = None
    active: bool | None = None


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    tax: Decimal | None = None
    active: Decimal | None = None
    category_id: uuid.UUID | None = None
    image: str | None = None


class ProductInDB(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: Decimal
    tax: Decimal
    image: str
    category_id: uuid.UUID
    category: CategoryInDB

    class Config:
        from_attributes = True

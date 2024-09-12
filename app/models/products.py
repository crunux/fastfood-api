from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from app.models.categories import Category

import uuid


class ProductBase(SQLModel):
    name: str
    description: str = ""
    price: Decimal
    tax: Decimal = 0.0
    active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da",
                "name": "Hamburguer",
                "description": "Hamburguer with cheese and bacon",
                "price": 10.5,
                "tax": 10.5 * 0.18,
                "active": True,
                "category_id": "0d5a87e1-9891-42a4-ba90-2e72e3a9e496",
            }
        }


class Product(ProductBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID | None = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    details_orders: list['DetailsOrder'] = Relationship(
        back_populates="product")


class ProductCreate(ProductBase):
    category_id: uuid.UUID | None = None
    tax: Decimal | None = None
    active: bool | None = None


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    tax: Decimal | None = None
    active: Decimal | None = None
    category_id: uuid.UUID | None = None


class ProductInDB(ProductBase):
    id: uuid.UUID
    category_id: uuid.UUID
    category: Category

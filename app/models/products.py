from sqlmodel import SQLModel, Field, Relationship
from app.models.categories import Category
from app.utils.generic_models import ProductCategory
import uuid


class ProductBase(SQLModel):
    name: str
    description: str = ""
    price: float
    tax: float = 0.0
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
    category_id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, foreign_key="category.id")
    category: Category = Relationship(
        back_populates="products", link_model=ProductCategory)


class ProductCreate(ProductBase):
    category_id: uuid.UUID | None = None
    tax: float | None = None,
    active: bool | None = None
    pass


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None
    active: bool | None = None
    category_id: uuid.UUID | None = None


class ProductInDB(ProductBase):
    id: uuid.UUID
    category_id: uuid.UUID
    category: Category | None = {}

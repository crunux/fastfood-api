from sqlmodel import SQLModel, Field, Relationship
import uuid
from app.utils.generic_models import ProductCategory


class CategoryBase(SQLModel):
    name: str
    description: str = ""

    class Config:
        json_schema_extra = {
            "example": {
                "id": "16fd2706-8baf-433b-82eb-8c7fada847da",
                "name": "Food",
                "description": "Food category",
                "products": [
                    "16fd2706-8baf-433b-82eb-8c7fada847da",
                    "16fd2706-8baf-433b-82eb-8c7fada847da",
                    "16fd2706-8baf-433b-82eb-8c7fada847da",
                ]
            }
        }


class Category(CategoryBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    products: list['Product'] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryInDB(CategoryBase):
    id: uuid.UUID
    name: str
    description: str = ""


class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None

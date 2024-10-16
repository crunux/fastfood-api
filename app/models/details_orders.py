
from typing import TYPE_CHECKING
import uuid
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from app.models.products import Product, ProductInDB

if TYPE_CHECKING:
    from app.models.orders import Order


class DetailsOrderBase(SQLModel):
    product_id: uuid.UUID
    order_id: uuid.UUID
    quantity: int = 1


class DetailsOrder(DetailsOrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,
                          primary_key=True, index=True)
    order_id: uuid.UUID = Field(
        default=uuid.UUID, foreign_key="order.id", index=True)
    product_id: uuid.UUID = Field(
        default=uuid.UUID, foreign_key="product.id", index=True)
    quantity: int = Field(default=1)
    product: Product = Relationship(back_populates="details_orders")
    order: "Order" = Relationship(
        back_populates="details_orders")


class DetailsOrderCreate(DetailsOrderBase):
    order_id: uuid.UUID | None = None

class DetailsOrderUpdate(DetailsOrderBase):
    quantity: int | None = None

class DetailsOrderInDB(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    order_id: uuid.UUID
    quantity: int
    product: ProductInDB

    class Config:
        from_attributes = True

from datetime import datetime
from enum import Enum
from app.models.details_orders import DetailsOrder, DetailsOrderCreate
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
import uuid


class StatusType(str, Enum):
    ordered = "ordered"
    completed = "completed"
    received = "received"
    cancelled = "cancelled"


class PaymentMethod(str, Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    cash = "cash"
    paypal = "paypal"
    bitcoin = "bitcoin"
    other = "other"


class DetailsProduct(SQLModel):
    product_id: uuid.UUID
    quantity: int = 1


class OrderBase(SQLModel):
    total_amount: Decimal = 0.0
    status: StatusType = Field(default=StatusType.ordered, index=False,
                               nullable=False)
    user_id: uuid.UUID
    order_date: datetime = Field(
        default=datetime.now, index=False, nullable=False)
    payment_method: PaymentMethod = Field(default=PaymentMethod.cash, index=False,
                                          nullable=False)
    shipping_address: str = ""
    total_tax: Decimal = 0.0


class Order(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    details_orders: list['DetailsOrder'] = Relationship(back_populates="order")


class OrderCreate(OrderBase):
    details_orders: list['DetailsOrder'] | None = None
    user_id: uuid.UUID | None = None
    total_amount: Decimal | None = None
    total_tax: Decimal | None = None


class OrderUpdate(OrderBase):
    status: StatusType | None = None
    total_amount: Decimal | None = None
    total_tax: Decimal | None = None
    user_id: uuid.UUID | None = None
    shipping_address: str | None = None


class OrderInDB(OrderBase):
    id: uuid.UUID
    total_amount: Decimal
    status: StatusType
    user_id: uuid.UUID
    order_date: datetime
    total_tax: Decimal
    details_orders: list["DetailsOrder"]
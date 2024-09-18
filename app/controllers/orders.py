from datetime import datetime
import uuid
from sqlmodel import Session, select
from fastapi import status, HTTPException
from app.models.details_orders import DetailsOrder, DetailsOrderCreate
from app.models.users import UserInDB
from app.controllers.products import get_product_by_id
from app.models.orders import Order, OrderCreate, OrderInDB, OrderUpdate
from sqlalchemy.orm import selectinload


def add_details_order(details_order: DetailsOrderCreate, db: Session) -> dict[str, int | float | str]:
    total_amount = 0
    total_tax = 0
    for detail in details_order:
        product = get_product_by_id(detail.product_id, db)
        total_amount += detail.quantity * product.price
        total_tax += detail.quantity * product.tax
    total_amount += total_tax
    return {"total_amount": total_amount, "total_tax": total_tax}


def create_order(order: OrderCreate, userAccess: UserInDB, db: Session) -> OrderInDB:
    detailsData = add_details_order(order.details_orders, db)
    extra_data = {
        "user_id": userAccess.id,
        "total_amount": detailsData["total_amount"],
        "total_tax": detailsData["total_tax"],
        "order_date": datetime.now(),
    }
    order = Order.model_validate(order, update=extra_data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session) -> list[OrderInDB]:
    # db_orders = db.exec(select(Order).offset(0).limit(100)).all()
    db_orders = db.exec(select(Order)).all()
    return db_orders


def get_order_by_id(order_id: uuid.UUID, db: Session) -> Order:
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return db_order


def update_order(order_id: uuid.UUID, order: OrderUpdate, db: Session) -> Order:
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    orderData = order.model_dump(exclude_unset=True)
    extra_data = {}
    if "details_orders" in orderData:
        detailsData = add_details_order(orderData["details_orders"], db)
        extra_data["total_amount"] = detailsData["total_amount"]
        extra_data["total_tax"] = detailsData["total_tax"]
    db_order.sqlmodel_update(orderData, update=extra_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(order_id: uuid.UUID, db: Session) -> dict:
    db_order = db.get(Order, order_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    db.delete(db_order)
    db.commit()
    return {"deleted": True, "message": f"Order {order_id} deleted"}

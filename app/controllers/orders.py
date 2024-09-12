from datetime import datetime
from sqlmodel import Session, select
from fastapi import status, HTTPException
from app.models.details_orders import DetailsOrder, DetailsOrderCreate
from app.models.users import UserInDB
from app.controllers.products import get_product_by_id
from app.models.orders import Order, OrderCreate, OrderInDB


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
    print("step 1", detailsData)  # debug
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

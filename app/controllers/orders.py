from datetime import datetime
from sqlmodel import Session, select
from fastapi import status, HTTPException
from app.models.details_orders import DetailsOrder, DetailsOrderCreate
from app.models.users import UserInDB
from app.controllers.products import get_product_by_id
from app.models.orders import Order, OrderCreate, OrderInDB


def create_order(order: OrderCreate, userAccess: UserInDB, db: Session) -> OrderInDB:
    detailsData = order.details_orders
    order.details_orders.delete()
    total_amount = 0
    total_tax = 0
    print("step 1", total_amount, total_tax)  # debug
    extra_data = {
        "user_id": userAccess.id,
        "total_amount": total_amount,
        "total_tax": total_tax,
        "order_date": datetime.now(),
    }
    order = Order.model_validate(order, update=extra_data)
    db.add(order)
    db.commit()
    for detail in detailsData:
        product = get_product_by_id(detail.product_id, db)
        total_amount += detail.quantity * product.price
        total_tax += detail.quantity * product.tax
        print("step 2", total_amount, total_tax)  # debug
        detailData = {"order_id": order.id,
                      "product_id": detail.product_id,
                      "quantity": detail.quantity
                      }
        db.add(DetailsOrder.model_validate(detailData))
        db.commit()
    total_amount += total_tax
    print("step 3", total_amount, total_tax)  # debug
    ordenData = order.model_dump(exclude_unset=True)
    order.sqlmodel_update(
        ordenData, update={"total_amount": total_amount, "total_tax": total_tax})
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

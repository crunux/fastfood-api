from sqlmodel import Session, select
from fastapi import status, HTTPException
import uuid
from app.models.details_orders import DetailsOrder, DetailsOrderCreate, DetailsOrderUpdate, DetailsOrderInDB
from app.database import get_session


def create_details_order(details_order: DetailsOrderCreate, db: Session) -> DetailsOrderInDB:

    details_order = DetailsOrder.model_validate(details_order)
    db.add(details_order)
    db.commit()
    db.refresh(details_order)
    return details_order

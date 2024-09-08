from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
import uuid
from app.database import get_session
from app.models.products import ProductCreate, ProductInDB
from app.controllers import create_product, get_products, get_product_by_id, update_product, delete_product


router = APIRouter(tags=["Products"], responses={
                   404: {"description": "Not found"}})


@router.post("", response_model=ProductInDB)
async def create_a_product(newProduct: ProductCreate, db: Session = Depends(get_session)) -> ProductInDB:
    return create_product(newProduct, db)


@router.get("", response_model=list[ProductInDB])
async def read_products(db: Session = Depends(get_session)) -> list[ProductInDB]:
    return get_products(db)


@router.get("/{product_id}", response_model=ProductInDB)
async def read_a_product(product_id: uuid.UUID, db: Session = Depends(get_session)) -> ProductInDB:
    # next((x for x in products_list if x["id"] == product_id), None)
    # next(filter(lambda x: x["id"] == product_id, products_list), None)
    return get_product_by_id(product_id, db)


@router.put("/{product_id}", response_model=ProductInDB)
async def update_a_product(product_id: uuid.UUID, product: ProductCreate, db: Session = Depends(get_session)) -> ProductInDB:
    return update_product(product_id, product, db)


@router.delete("/{product_id}", response_model=dict)
async def delete_a_product(product_id: uuid.UUID, db: Session = Depends(get_session)) -> dict:
    return delete_product(product_id, db)

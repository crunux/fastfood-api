from sqlmodel import Session, select
from fastapi import status, Depends, HTTPException
import uuid
from app.models.products import Product, ProductCreate, ProductUpdate, ProductInDB
from app.database import get_session


def create_product(product: ProductCreate, db: Session = Depends(get_session)) -> ProductInDB:
    product = Product.model_validate(product)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session = Depends(get_session)) -> list[ProductInDB]:
    statement = select(Product).order_by(Product.id)
    products = db.exec(statement).all()
    return products


def get_product_by_id(id: uuid.UUID, db: Session = Depends(get_session)) -> ProductInDB:
    statement = select(Product).where(Product.id == id)
    product = db.exec(statement).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")
    return product


def update_product(id: uuid.UUID, product: ProductUpdate, db: Session = Depends(get_session)) -> ProductInDB:

    productUpdate = db.get(Product, id)

    if not productUpdate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")

    productData = product.model_dump(exclude_unset=True)

    for key, value in productData.items():
        setattr(productUpdate, key, value)

    # statement = text(
    #     "UPDATE products SET name = :name, description = :description, price = :price WHERE id = :id")
    # db.exec(statement, {"id": id, **product.dict()})

    db.add(product)
    db.commit()
    db.refresh(product)
    return get_product_by_id(id, db)


def delete_product(id: uuid.UUID, db: Session = Depends(get_session)) -> dict:
    product = db.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id: {id}")

    db.delete(product)
    db.commit()
    return {"deleted": True, "message": f"Category {id} deleted"}

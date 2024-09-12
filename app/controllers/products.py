from sqlmodel import Session, select
from fastapi import status, Depends, HTTPException
import uuid
from app.models.products import Product, ProductCreate, ProductUpdate, ProductInDB
from app.models.users import UserInDB


def create_product(product: ProductCreate, db: Session) -> ProductInDB:
    extra_data = {
        "tax": round(product.price * 0.18, 2)
    }
    product = Product.model_validate(product, update=extra_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(acessUser: UserInDB, db: Session) -> list[ProductInDB]:
    products = db.exec(select(Product)).all()
    return products


def get_product_by_id(id: uuid.UUID, db: Session) -> ProductInDB:
    product = db.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found")
    return product


def update_product(id: uuid.UUID, product: ProductUpdate, db: Session) -> ProductInDB:
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    productData = product.model_dump(exclude_unset=True)
    extra_data = {}
    if "price" in productData:
        extra_data["tax"] = round(productData["price"] * 0.18, 2)
    db_product.sqlmodel_update(productData, update=extra_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(id: uuid.UUID, db: Session) -> dict:
    product = db.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"deleted": True, "message": f"Category {id} deleted"}

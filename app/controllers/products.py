import os
import uuid
from app.config import settings
from sqlmodel import Session, select
from fastapi import UploadFile, status, HTTPException
from app.models.products import Product, ProductCreate, ProductUpdate, ProductInDB
from app.models.users import UserInDB

UPLOAD_DIR = "img/products/"

os.makedirs(UPLOAD_DIR, exist_ok=True)



async def create_product(product: ProductCreate, file: UploadFile, db: Session) -> ProductInDB:
    
    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Only images allowed ''jpeg' or 'png'")
    
        file_name = f'{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}'
        file_name_dir = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_name_dir, "wb") as buffer:
            buffer.write(await file.read())
        
        extra_data = {
            "tax": round(product.price * 0.18, 2),
            "image": ("",file_name)[file] 
        }
    else: 
        extra_data = {
            "tax": round(product.price * 0.18, 2),
            "image": ""
        }
    product = Product.model_validate(product, update=extra_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    product = {
      "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "tax": product.tax,
        "active": product.active,
        "image": (product.image, f"{settings.SERVER_HOST}/{UPLOAD_DIR}{product.image}")[product.image != ""]
        
    }
    return product


def get_products(acessUser: UserInDB, db: Session) -> list[ProductInDB]:
    products = db.exec(select(Product)).all()
    if len(products)  == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not found")
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

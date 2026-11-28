from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from application.store import find_product, list_products
from config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Focused e-commerce API for the Docker engineering journey.",
)
# Phase 4 cache test
# phase 4 bad main.py update test 
# phase 6 v2 edit
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

class OrderRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)

class OrderResponse(BaseModel):
    order_id: int
    status: str
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total: float

@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "environment": settings.environment,
        "status": "running",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return list_products()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest):
    product = find_product(order.product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    total = round(product["price"] * order.quantity, 2)

    return {
        "order_id": 1001,
        "status": "created",
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order.quantity,
        "unit_price": product["price"],
        "total": total,
    }

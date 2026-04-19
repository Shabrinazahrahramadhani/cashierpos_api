from fastapi import FastAPI
from database import engine, Base

from models.user import User
from models.product import Category, Product, Transaction, TransactionItem

from routers import auth, categories, products, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CashierPos API",
    description="Sistem Kasir & Manajemen Produk berbasis RESTful API",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(transactions.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "CashierPos API berjalan!",
        "docs": "/docs"
    }
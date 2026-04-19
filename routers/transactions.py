from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product import Product, Transaction, TransactionItem
from schemas.transaction import TransactionCreate, TransactionResponse
from security.dependencies import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total_price = 0.0
    item_details = []

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produk ID {item.product_id} tidak ditemukan")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stok '{product.name}' tidak mencukupi")
        subtotal = product.price * item.quantity
        total_price += subtotal
        item_details.append({"product": product, "quantity": item.quantity, "subtotal": subtotal})

    transaction = Transaction(total_price=total_price, cashier_id=current_user.id)
    db.add(transaction)
    db.flush()

    for detail in item_details:
        tx_item = TransactionItem(
            transaction_id=transaction.id,
            product_id=detail["product"].id,
            quantity=detail["quantity"],
            subtotal=detail["subtotal"]
        )
        db.add(tx_item)
        detail["product"].stock -= detail["quantity"]

    db.commit()
    db.refresh(transaction)
    return transaction


@router.get("/", response_model=List[TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Transaction).all()


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaksi ID {transaction_id} berhasil dihapus"}
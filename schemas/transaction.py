from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TransactionItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class TransactionCreate(BaseModel):
    items: List[TransactionItemCreate] = Field(..., min_length=1)


class TransactionItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: int
    total_price: float
    cashier_id: int
    created_at: datetime
    items: List[TransactionItemResponse] = []

    class Config:
        from_attributes = True
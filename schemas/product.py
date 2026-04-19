from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category_id: int
    category: Optional[CategoryResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
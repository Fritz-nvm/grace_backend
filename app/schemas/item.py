from pydantic import BaseModel, Field, condecimal
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2) = Field(..., gt=0)
    sale_price: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(
        None, gt=0
    )
    sku: Optional[str] = Field(None, max_length=100)
    images: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    sizes: List[str] = Field(default_factory=list)
    fabric: Optional[str] = Field(None, max_length=100)
    stock_quantity: int = Field(default=0, ge=0)
    is_available: bool = True
    collection_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(None, gt=0)
    sale_price: Optional[condecimal(max_digits=10, decimal_places=2)] = Field(
        None, gt=0
    )
    sku: Optional[str] = Field(None, max_length=100)
    images: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    fabric: Optional[str] = Field(None, max_length=100)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None
    collection_id: Optional[int] = None


class ItemResponse(ItemBase):
    id: int
    slug: str
    likes_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

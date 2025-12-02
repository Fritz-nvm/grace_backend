from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, validator
import uuid
import json
import re


class ItemBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = None
    images: Optional[List[str]] = Field(default_factory=list)
    colors: Optional[List[str]] = Field(default_factory=list)
    sizes: Optional[List[str]] = Field(default_factory=list)
    fabric: Optional[str] = Field(None, max_length=100)
    fabric_composition: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = None
    collection_id: uuid.UUID


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = None
    images: Optional[List[str]] = Field(default_factory=list)
    colors: Optional[List[str]] = Field(default_factory=list)
    sizes: Optional[List[str]] = Field(default_factory=list)
    fabric: Optional[str] = Field(None, max_length=100)
    fabric_composition: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = None
    collection_id: Optional[uuid.UUID] = None


class ItemInDBBase(ItemBase):
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    collection_name: Optional[str] = None

    class Config:
        from_attributes = True


class Item(ItemInDBBase):
    pass


ItemResponse = Item

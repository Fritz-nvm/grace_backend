from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.item import Item


class CollectionBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = True
    display_order: Optional[int] = 0
    suite_id: int


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None
    suite_id: Optional[int] = None


class CollectionInDBBase(CollectionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Collection(CollectionInDBBase):
    # Option 1: List of item IDs (simple, avoids circular imports)
    item_ids: List[int] = []

    # Option 2: Full item objects (if you want complete item data)
    # items: List[Item] = []

    class Config:
        from_attributes = True


CollectionResponse = Collection

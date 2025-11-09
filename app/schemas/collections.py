from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CollectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class CollectionResponse(CollectionBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

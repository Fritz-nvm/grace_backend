from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import uuid


class PackageBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: Decimal = Field(..., gt=0)
    description: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    pdf_url: Optional[str] = Field(None, max_length=512)
    is_active: bool = True
    display_order: int = Field(0, ge=0)
    is_popular: bool = False


class PackageCreate(PackageBase):
    """Schema for creating a new Package."""

    pass


class PackageUpdate(BaseModel):
    """Schema for updating an existing Package (all fields are optional)."""

    name: Optional[str] = Field(None, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = None
    featurees: Optional[List[str]] = None
    pdf_url: Optional[str] = Field(None, max_length=512)
    is_active: Optional[bool] = None
    display_order: Optional[int] = Field(None, ge=0)
    is_popular: Optional[bool] = None


class PackageOut(PackageBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    package_name: Optional[str]
    download_link: Optional[str]

    class Config:
        from_attributes = True

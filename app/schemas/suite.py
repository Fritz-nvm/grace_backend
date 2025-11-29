from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.collection import Collection


class SuiteBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = True


class SuiteCreate(SuiteBase):
    pass


class SuiteUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SuiteInDBBase(SuiteBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Suite(SuiteInDBBase):
    pass


SuiteResponse = Suite

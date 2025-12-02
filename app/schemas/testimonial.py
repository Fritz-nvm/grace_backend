# app/schemas/testimonial.py
from typing import Optional
from pydantic import BaseModel, Field, validator, ConfigDict
from datetime import datetime
import uuid
from decimal import Decimal


class TestimonialBase(BaseModel):
    """Base schema for Testimonial"""

    client_name: str = Field(
        ..., min_length=1, max_length=100, description="Full name of the client"
    )
    review_text: Optional[str] = Field(
        None, max_length=2000, description="Testimonial text content"
    )
    rating: int = Field(0, ge=0, le=5, description="Rating from 0 to 5 stars")
    display_order: int = Field(0, ge=0, description="Sorting order for display")

    @validator("client_name")
    def validate_client_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Client name cannot be empty")
        return v

    @validator("review_text")
    def validate_review_text(cls, v):
        if v is not None:
            v = v.strip()
            if len(v) < 10:
                raise ValueError("Review text must be at least 10 characters")
        return v


class TestimonialCreate(TestimonialBase):
    """Schema for creating testimonials"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_name": "Jane Smith",
                "review_text": "Absolutely stunning designs! The quality exceeded my expectations.",
                "rating": 5,
                "display_order": 1,
            }
        }
    )


class TestimonialUpdate(BaseModel):
    """Schema for updating testimonials - all fields optional"""

    client_name: Optional[str] = Field(None, min_length=1, max_length=100)
    review_text: Optional[str] = Field(None, max_length=2000)
    rating: Optional[int] = Field(None, ge=0, le=5)
    display_order: Optional[int] = Field(None, ge=0)

    model_config = ConfigDict(
        json_schema_extra={"example": {"client_name": "Jane Updated", "rating": 4}}
    )


class TestimonialInDB(TestimonialBase):
    """Schema for database records"""

    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TestimonialResponse(TestimonialInDB):
    """Schema for API responses"""

    pass


class TestimonialList(BaseModel):
    """Schema for listing testimonials"""

    testimonials: list[TestimonialResponse]
    total: int
    page: int
    size: int
    pages: int

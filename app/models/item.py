from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    ARRAY,
    Numeric,
    Enum,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base
from typing import List
import enum

import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.db_types import ListStringType


class CategoryEnum(enum.Enum):
    bridal = "bridal"
    boutique = "boutique"


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    price = Column(Numeric(10, 2), nullable=False)

    colors: Mapped[List[str]] = mapped_column(ListStringType(length=255))
    sizes: Mapped[List[str]] = mapped_column(ListStringType(length=255))
    images: Mapped[List[str]] = mapped_column(
        ListStringType(length=512)
    )  # For multiple image URLs/paths

    fabric = Column(String(100))
    fabric_composition = Column(String(255))
    category = Column(Enum(CategoryEnum))

    # Foreign key
    collection_id = Column(
        UUID(as_uuid=True), ForeignKey("collections.id", ondelete="CASCADE")
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    collection = relationship("Collection", back_populates="items", lazy="joined")

    @property
    def collection_name(self):
        return self.collection.name if self.collection else None

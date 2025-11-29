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
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class CategoryEnum(enum.Enum):
    BRIDAL = "BRIDAL"
    BOUTIQUE = "BOUTIQUE"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    price = Column(Numeric(10, 2), nullable=False)

    images = Column(ARRAY(String), default=list)
    colors = Column(ARRAY(String), default=list)
    sizes = Column(ARRAY(String), default=list)
    fabric = Column(String(100))
    fabric_composition = Column(String(255))
    category = Column(Enum(CategoryEnum))

    # Foreign key
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    collection = relationship("Collection", back_populates="items")

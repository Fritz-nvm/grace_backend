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
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    description = Column(Text)

    # Pricing
    price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=True)

    # Product details
    images = Column(ARRAY(String), default=list)  # Multiple image URLs
    colors = Column(ARRAY(String), default=list)
    sizes = Column(ARRAY(String), default=list)
    fabric = Column(String(100))

    # Inventory
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)

    # Social
    likes_count = Column(Integer, default=0)

    # Foreign key
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    collection = relationship("Collection", back_populates="items")

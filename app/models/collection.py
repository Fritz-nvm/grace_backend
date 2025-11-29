# app/models/collection.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship

    suite_id = Column(Integer, ForeignKey("suite.id"))  # Add suite foreign key

    suite = relationship("Suite", back_populates="collections")
    items = relationship(
        "Item", back_populates="collection", cascade="all, delete-orphan"
    )

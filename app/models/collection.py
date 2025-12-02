# app/models/collection.py
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID


class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship

    suite_id = Column(UUID(as_uuid=True), ForeignKey("suite.id", ondelete="CASCADE"))

    suite = relationship("Suite", back_populates="collections", lazy="joined")
    items = relationship(
        "Item", back_populates="collection", cascade="all, delete-orphan"
    )

    @property
    def suite_name(self):
        return self.suite.name if self.suite else None

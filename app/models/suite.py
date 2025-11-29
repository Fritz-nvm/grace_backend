from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Suite(Base):
    __tablename__ = "suite"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    collections = relationship(
        "Collection", back_populates="suite", cascade="all, delete-orphan"
    )

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base  # Assuming this import is correct

import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.db_types import ListStringType
from sqlalchemy.orm import Mapped, mapped_column
from typing import List


class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    features: Mapped[List[str]] = mapped_column(ListStringType(length=255))
    pdf_url = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_popular = Column(Boolean, default=False)

    @property
    def package_name(self):
        return self.name if self.name else None

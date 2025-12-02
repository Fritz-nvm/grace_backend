from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, inspect
from sqlalchemy.ext.declarative import declarative_base

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class that provides default CRUD operations for a given SQLAlchemy model.
    Methods handle fetching, creating, updating, and deleting objects.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Fetch a single object by ID."""
        stmt = select(self.model).filter(self.model.id == id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Fetch a list of objects."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
        # Convert Pydantic object to dictionary, excluding unset values
        obj_in_data = (
            obj_in.model_dump()
            if hasattr(obj_in, "model_dump")
            else jsonable_encoder(obj_in)
        )

        # Filter data to only include columns defined in the model
        # Using inspect(self.model).columns for dynamic column names
        model_column_names = [c.key for c in inspect(self.model).columns]

        # NOTE: Relationship filtering is handled here, but may need adjustment
        # depending on your specific model relationships.
        relationship_names = ["collections", "items"]

        filtered_data = {
            k: v
            for k, v in obj_in_data.items()
            if k in model_column_names and k not in relationship_names
        }

        db_obj = self.model(**filtered_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing object."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Pydantic v2 .model_dump(exclude_unset=True)
            update_data = (
                obj_in.model_dump(exclude_unset=True)
                if hasattr(obj_in, "model_dump")
                else obj_in.dict(exclude_unset=True)
            )

        # Filter data to only include columns defined in the model
        model_column_names = [c.key for c in inspect(self.model).columns]
        relationship_names = ["collections", "items"]

        filtered_data = {
            k: v
            for k, v in update_data.items()
            if k in model_column_names and k not in relationship_names
        }

        for field, value in filtered_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """Remove an object by ID."""
        stmt = select(self.model).filter(self.model.id == id)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

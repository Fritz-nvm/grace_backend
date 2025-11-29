from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate


class CollectionCRUD:
    async def create(self, db: AsyncSession, *, obj_in: CollectionCreate) -> Collection:
        """
        Create a new collection.
        """
        db_collection = Collection(
            name=obj_in.name,
            description=obj_in.description,
            is_active=getattr(obj_in, "is_active", True),
            display_order=getattr(obj_in, "display_order", 0),
            suite_id=obj_in.suite_id,
        )
        db.add(db_collection)
        await db.commit()

        stmt = (
            select(Collection)
            .options(selectinload(Collection.items), selectinload(Collection.suite))
            .filter(Collection.id == db_collection.id)
        )
        result = await db.execute(stmt)
        loaded = result.scalars().first()
        if loaded:
            await db.refresh(loaded)
            return loaded

        # Fallback
        await db.refresh(db_collection)
        return db_collection

    async def get(self, db: AsyncSession, collection_id: int) -> Optional[Collection]:
        """
        Get a collection by ID with items eagerly loaded.
        """
        stmt = (
            select(Collection)
            .options(selectinload(Collection.items))
            .filter(Collection.id == collection_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_suite(
        self, db: AsyncSession, *, suite_id: int, skip: int = 0, limit: int = 100
    ) -> List[Collection]:
        """
        Get all collections for a specific suite.
        """
        stmt = (
            select(Collection)
            .options(selectinload(Collection.items))
            .filter(Collection.suite_id == suite_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Collection]:
        """
        Get all collections.
        """
        stmt = (
            select(Collection)
            .options(selectinload(Collection.items))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: Collection, obj_in: CollectionUpdate
    ) -> Collection:
        """
        Update a collection.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(
        self, db: AsyncSession, *, collection_id: int
    ) -> Optional[Collection]:
        """
        Delete a collection.
        """
        stmt = select(Collection).filter(Collection.id == collection_id)
        result = await db.execute(stmt)
        db_collection = result.scalars().first()
        if db_collection:
            await db.delete(db_collection)
            await db.commit()
        return db_collection


# Create an instance of the CollectionCRUD class
collection = CollectionCRUD()

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
import uuid


class ItemCRUD:
    async def create(self, db: AsyncSession, *, obj_in: ItemCreate) -> Item:
        """
        Create a new item. Ensure array fields are passed as Python lists (not JSON strings).
        """
        # Ensure list types (Pydantic should already give lists, but be defensive)
        images = obj_in.images or []
        colors = obj_in.colors or []
        sizes = obj_in.sizes or []

        db_item = Item(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            images=images,
            colors=colors,
            sizes=sizes,
            fabric=obj_in.fabric,
            fabric_composition=obj_in.fabric_composition,
            category=obj_in.category,
            collection_id=obj_in.collection_id,
        )
        db.add(db_item)
        try:
            await db.commit()
            await db.refresh(db_item)
        except IntegrityError as exc:
            await db.rollback()
            # surface a friendly error (FK/enum/unique violations)
            raise HTTPException(status_code=400, detail=str(exc.orig)) from exc

        return db_item

    async def get(self, db: AsyncSession, *, item_id: uuid.UUID) -> Optional[Item]:
        """
        Get an item by ID with collection relationship eagerly loaded.
        """
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .filter(Item.id == item_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_collection(
        self,
        db: AsyncSession,
        *,
        collection_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .filter(Item.collection_id == collection_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "-created_at"
    ) -> List[Item]:
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .offset(skip)
            .limit(limit)
        )

        if order_by.startswith("-"):
            field = getattr(Item, order_by[1:])
            stmt = stmt.order_by(field.desc())
        else:
            field = getattr(Item, order_by)
            stmt = stmt.order_by(field.asc())

        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: Item, obj_in: ItemUpdate
    ) -> Item:
        """
        Update an item. Accept lists for array fields.
        """
        update_data = obj_in.dict(exclude_unset=True)

        # Defensive: ensure array fields are proper lists
        if "images" in update_data and update_data["images"] is not None:
            update_data["images"] = list(update_data["images"])
        if "colors" in update_data and update_data["colors"] is not None:
            update_data["colors"] = list(update_data["colors"])
        if "sizes" in update_data and update_data["sizes"] is not None:
            update_data["sizes"] = list(update_data["sizes"])

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        try:
            await db.commit()
            await db.refresh(db_obj)
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc.orig)) from exc

        return db_obj

    async def delete(self, db: AsyncSession, *, item_id: uuid.UUID) -> Optional[Item]:
        stmt = select(Item).filter(Item.id == item_id)
        result = await db.execute(stmt)
        db_item = result.scalars().first()
        if db_item:
            await db.delete(db_item)
            await db.commit()
        return db_item


# Create an instance of the ItemCRUD class
item = ItemCRUD()

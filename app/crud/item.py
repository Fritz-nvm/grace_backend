from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemCRUD:
    async def create(self, db: AsyncSession, *, obj_in: ItemCreate) -> Item:
        """
        Create a new item.
        """
        db_item = Item(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            images=obj_in.images or [],  # Direct list for ARRAY column
            colors=obj_in.colors or [],  # Direct list for ARRAY column
            sizes=obj_in.sizes or [],  # Direct list for ARRAY column
            fabric=obj_in.fabric,
            fabric_composition=obj_in.fabric_composition,
            category=obj_in.category,
            collection_id=obj_in.collection_id,
        )
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    async def get(self, db: AsyncSession, item_id: int) -> Optional[Item]:
        """
        Get an item by ID.
        """
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .filter(Item.id == item_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_collection(
        self, db: AsyncSession, *, collection_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        Get all items for a specific collection.
        """
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
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        Get all items.
        """
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: Item, obj_in: ItemUpdate
    ) -> Item:
        """
        Update an item.
        """
        update_data = obj_in.dict(exclude_unset=True)

        # No need for json.dumps() - ARRAY columns take lists directly
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, item_id: int) -> Optional[Item]:
        """
        Delete an item.
        """
        stmt = select(Item).filter(Item.id == item_id)
        result = await db.execute(stmt)
        db_item = result.scalars().first()
        if db_item:
            await db.delete(db_item)
            await db.commit()
        return db_item

    async def get_by_category(
        self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        Get items by category.
        """
        stmt = (
            select(Item)
            .options(selectinload(Item.collection))
            .filter(Item.category == category)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()


# Create an instance of the ItemCRUD class
item = ItemCRUD()

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify
from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: ItemCreate) -> Item:
        obj_in_data = obj_in.model_dump()
        # Generate slug from name
        obj_in_data["slug"] = slugify(obj_in_data["name"])
        db_obj = Item(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Item]:
        result = await db.execute(select(Item).where(Item.slug == slug))
        return result.scalar_one_or_none()

    async def get_by_collection(
        self, db: AsyncSession, collection_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        result = await db.execute(
            select(Item)
            .where(Item.collection_id == collection_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_available(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Item)
            .where(Item.is_available == True)
            .where(Item.stock_quantity > 0)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def increment_likes(self, db: AsyncSession, item_id: int) -> Optional[Item]:
        item = await self.get(db, item_id)
        if item:
            item.likes_count += 1
            await db.commit()
            await db.refresh(item)
        return item


item = CRUDItem(Item)

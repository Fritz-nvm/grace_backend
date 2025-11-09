from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify
from app.crud.base import CRUDBase
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate, CollectionUpdate


class CRUDCollection(CRUDBase[Collection, CollectionCreate, CollectionUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: CollectionCreate) -> Collection:
        obj_in_data = obj_in.model_dump()
        # Generate slug from name
        obj_in_data["slug"] = slugify(obj_in_data["name"])
        db_obj = Collection(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Collection]:
        result = await db.execute(select(Collection).where(Collection.slug == slug))
        return result.scalar_one_or_none()

    async def get_active(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Collection)
            .where(Collection.is_active == True)
            .order_by(Collection.display_order)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


collection = CRUDCollection(Collection)

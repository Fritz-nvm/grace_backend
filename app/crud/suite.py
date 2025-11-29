from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.suite import Suite
from app.schemas.suite import SuiteCreate, SuiteUpdate


class SuiteCRUD:
    async def create(self, db: AsyncSession, *, obj_in: SuiteCreate) -> Suite:
        """
        Create a new suite.
        """
        db_suite = Suite(
            name=obj_in.name,
            description=obj_in.description,
            is_active=getattr(obj_in, "is_active", True),
        )
        db.add(db_suite)
        await db.commit()
        await db.refresh(db_suite)
        return db_suite

    async def get(self, db: AsyncSession, suite_id: int) -> Optional[Suite]:
        """
        Get a suite by ID with collections eagerly loaded.
        """
        stmt = (
            select(Suite)
            .options(selectinload(Suite.collections))
            .filter(Suite.id == suite_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_all(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Suite]:
        """
        Get all suites with collections eagerly loaded.
        """
        stmt = (
            select(Suite)
            .options(selectinload(Suite.collections))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: Suite, obj_in: SuiteUpdate
    ) -> Suite:
        """
        Update a suite.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, suite_id: int) -> Optional[Suite]:
        """
        Delete a suite.
        """
        stmt = select(Suite).filter(Suite.id == suite_id)
        result = await db.execute(stmt)
        db_suite = result.scalars().first()
        if db_suite:
            await db.delete(db_suite)
            await db.commit()
        return db_suite

    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Suite]:
        """
        Get a suite by name.
        """
        stmt = select(Suite).filter(Suite.name == name)
        result = await db.execute(stmt)
        return result.scalars().first()


# Create an instance of the SuiteCRUD class
suite = SuiteCRUD()

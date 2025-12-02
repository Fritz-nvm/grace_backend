# app/crud/testimonial.py
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.expression import func

from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate


class TestimonialNotFoundError(Exception):
    """Raised when a testimonial is not found"""

    pass


class TestimonialAlreadyExistsError(Exception):
    """Raised when a testimonial with same client name already exists"""

    pass


class TestimonialCRUD:
    """
    CRUD operations for the Testimonial model.
    """

    # --- CREATE ---
    async def create(
        self, db: AsyncSession, *, obj_in: TestimonialCreate
    ) -> Testimonial:
        """
        Create a new Testimonial.
        """
        # Check if a testimonial with the same client name already exists
        if await self.exists_by_client_name(db, client_name=obj_in.client_name):
            raise TestimonialAlreadyExistsError(
                f"A testimonial for client '{obj_in.client_name}' already exists."
            )

        try:
            # Convert Pydantic object to model instance
            db_testimonial = Testimonial(**obj_in.model_dump())
            db.add(db_testimonial)
            await db.commit()
            await db.refresh(db_testimonial)
            return db_testimonial
        except IntegrityError as e:
            await db.rollback()
            raise TestimonialAlreadyExistsError(
                f"Integrity Error: A testimonial conflict occurred."
            ) from e

    # --- READ ONE by ID ---
    async def get_by_id(self, db: AsyncSession, testimonial_id: UUID) -> Testimonial:
        """
        Get a testimonial by UUID. Raises TestimonialNotFoundError if not found.
        """
        stmt = select(Testimonial).filter(Testimonial.id == testimonial_id)
        result = await db.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise TestimonialNotFoundError(
                f"Testimonial with ID '{testimonial_id}' not found."
            )

    # --- READ ONE by Client Name ---
    async def get_by_client_name(
        self, db: AsyncSession, *, client_name: str
    ) -> Optional[Testimonial]:
        """
        Get a testimonial by client name (case-insensitive).
        """
        stmt = select(Testimonial).filter(
            func.lower(Testimonial.client_name) == func.lower(client_name)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    # --- READ ALL ---
    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "display_order",  # or "-created_at", "rating", etc.
    ) -> List[Testimonial]:
        """
        Get all testimonials with optional ordering.
        """
        # Parse order_by parameter
        if order_by.startswith("-"):
            field_name = order_by[1:]
            order = getattr(Testimonial, field_name).desc()
        else:
            field_name = order_by
            order = getattr(Testimonial, field_name).asc()

        # Ensure the field exists, default to display_order
        if not hasattr(Testimonial, field_name):
            order = Testimonial.display_order.asc()

        stmt = select(Testimonial).order_by(order).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    # --- UPDATE ---
    async def update(
        self, db: AsyncSession, *, testimonial_id: UUID, obj_in: TestimonialUpdate
    ) -> Testimonial:
        """
        Update a testimonial.
        """
        # 1. Retrieve the existing testimonial
        db_obj = await self.get_by_id(db, testimonial_id)

        update_data = obj_in.model_dump(exclude_unset=True)

        # 2. Check for client name conflict if updating client_name
        if (
            "client_name" in update_data
            and update_data["client_name"] != db_obj.client_name
        ):
            if await self.exists_by_client_name(
                db, client_name=update_data["client_name"]
            ):
                raise TestimonialAlreadyExistsError(
                    f"Update failed: A testimonial for client '{update_data['client_name']}' already exists."
                )

        # 3. Apply updates
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise TestimonialAlreadyExistsError(
                "Update failed due to a database integrity constraint."
            ) from e

    # --- DELETE ---
    async def delete(self, db: AsyncSession, *, testimonial_id: UUID) -> None:
        """
        Delete a testimonial by UUID.
        """
        db_testimonial = await self.get_by_id(db, testimonial_id)

        await db.delete(db_testimonial)
        await db.commit()

    # --- SEARCH ---
    async def search(
        self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Testimonial]:
        """
        Search testimonials by client name or review text (case-insensitive).
        """
        search_term = f"%{query}%"
        stmt = (
            select(Testimonial)
            .filter(
                func.lower(Testimonial.client_name).like(func.lower(search_term))
                | func.lower(Testimonial.review_text).like(func.lower(search_term))
            )
            .order_by(Testimonial.display_order)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    # --- Get by Rating ---
    async def get_by_rating(
        self,
        db: AsyncSession,
        *,
        min_rating: int = 0,
        max_rating: int = 5,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Testimonial]:
        """
        Get testimonials within a rating range.
        """
        stmt = (
            select(Testimonial)
            .filter(Testimonial.rating >= min_rating, Testimonial.rating <= max_rating)
            .order_by(Testimonial.rating.desc(), Testimonial.display_order)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    # --- Get Count ---
    async def get_count(self, db: AsyncSession) -> int:
        """
        Get total number of testimonials.
        """
        stmt = select(func.count()).select_from(Testimonial)
        result = await db.execute(stmt)
        return result.scalar_one()


testimonial = TestimonialCRUD()

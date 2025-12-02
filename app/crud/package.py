from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.expression import func

from app.models.package import Package
from app.schemas.package import PackageCreate, PackageUpdate
from app.exceptions.package import PackageNotFoundError, PackageAlreadyExistsError


class PackageNotFoundError(Exception):
    pass


class PackageAlreadyExistsError(Exception):
    pass


class PackageCRUD:
    """
    CRUD operations for the Package model, providing dedicated methods
    for common database interactions and handling application-specific exceptions.
    """

    # --- CREATE ---
    async def create(self, db: AsyncSession, *, obj_in: PackageCreate) -> Package:
        """
        Create a new Package.
        """
        # 1. Check if a package with the same name already exists
        if await self.exists_by_name(db, name=obj_in.name):
            raise PackageAlreadyExistsError(
                f"A package named '{obj_in.name}' already exists."
            )

        try:
            # Convert Pydantic object to model instance
            db_package = Package(**obj_in.model_dump())
            db.add(db_package)
            await db.commit()
            await db.refresh(db_package)
            return db_package
        except IntegrityError as e:
            await db.rollback()
            # Catch remaining IntegrityError (e.g., if another process created it concurrently)
            raise PackageAlreadyExistsError(
                f"Integrity Error: A package name conflict occurred."
            ) from e

    # --- READ ONE by ID ---
    async def get_by_id(self, db: AsyncSession, package_id: UUID) -> Package:
        """
        Get a package by UUID. Raises PackageNotFoundError if not found.
        """
        stmt = select(Package).filter(Package.id == package_id)
        result = await db.execute(stmt)

        try:
            return result.scalar_one()
        except NoResultFound:
            raise PackageNotFoundError(f"Package with ID '{package_id}' not found.")

    # --- READ ONE by Name ---
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Package]:
        """
        Get a package by name.
        """
        stmt = select(Package).filter(Package.name == name)
        result = await db.execute(stmt)
        return result.scalars().first()

    # --- READ ALL ---
    async def get_all(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Package]:
        """
        Get all packages, ordered by display_order.
        """
        stmt = select(Package).order_by(Package.display_order).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    # --- UPDATE ---
    async def update(
        self, db: AsyncSession, *, package_id: UUID, obj_in: PackageUpdate
    ) -> Package:
        """
        Update a package.
        """
        # 1. Retrieve the existing package (raises error if not found)
        db_obj = await self.get_by_id(db, package_id)

        update_data = obj_in.model_dump(exclude_unset=True)

        # 2. Check for name conflict if name is being updated
        if "name" in update_data and update_data["name"] != db_obj.name:
            if await self.exists_by_name(db, name=update_data["name"]):
                raise PackageAlreadyExistsError(
                    f"Update failed: A package named '{update_data['name']}' already exists."
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
            # Fallback catch for DB-level integrity violations
            raise PackageAlreadyExistsError(
                "Update failed due to a database integrity constraint."
            ) from e

    # --- DELETE ---
    async def delete(self, db: AsyncSession, *, package_id: UUID) -> None:
        """
        Delete a package by UUID. Raises PackageNotFoundError if not found.
        """
        db_package = await self.get_by_id(db, package_id)

        await db.delete(db_package)
        await db.commit()
        # Returns None implicitly as status code 204 is handled by the API endpoint

    # --- EXISTS Check by ID ---
    async def exists(self, db: AsyncSession, *, package_id: UUID) -> bool:
        """
        Check if a package exists by UUID.
        """
        stmt = select(Package.id).filter(Package.id == package_id)
        result = await db.execute(stmt)
        return result.scalar() is not None

    # --- EXISTS Check by Name ---
    async def exists_by_name(self, db: AsyncSession, *, name: str) -> bool:
        """
        Check if a package exists by name.
        """
        stmt = select(Package.id).filter(Package.name == name)
        result = await db.execute(stmt)
        return result.scalar() is not None

    # --- Search ---
    async def search_by_name(
        self, db: AsyncSession, *, name: str, skip: int = 0, limit: int = 100
    ) -> List[Package]:
        """
        Search packages by name (case-insensitive partial match).
        """
        stmt = (
            select(Package)
            .filter(func.lower(Package.name).like(f"%{name.lower()}%"))
            .order_by(Package.display_order)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()


package = PackageCRUD()

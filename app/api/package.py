from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

# Explicitly import get_db and use standard imports
from app.database import get_db
from app.crud.package import package as crud_package
from app.schemas.package import PackageCreate, PackageUpdate, PackageOut
from app.exceptions.package import PackageNotFoundError, PackageAlreadyExistsError


router = APIRouter()


@router.post(
    "/",
    response_model=PackageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new package",
)
async def create_package_endpoint(
    package_in: PackageCreate,
    db: AsyncSession = Depends(get_db),  # Inline dependency injection
):
    """
    Creates a new package with details including name, price, features, and an optional PDF URL path.
    """
    try:
        return await crud_package.create(db, obj_in=package_in)
    except PackageAlreadyExistsError as e:
        # Translate application error (name conflict) to 409 Conflict
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# --- GET /packages (Read All/List) ---
@router.get("/", response_model=List[PackageOut], summary="List all packages")
async def read_all_packages_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db),  # Inline dependency injection
):
    """
    Retrieves a list of all packages, allowing for pagination using skip and limit parameters.
    """
    return await crud_package.get_all(db=db, skip=skip, limit=limit)


# --- GET /packages/{package_id} (Read One by ID) ---
@router.get("/{package_id}", response_model=PackageOut, summary="Get package by ID")
async def read_package_by_id_endpoint(
    package_id: UUID, db: AsyncSession = Depends(get_db)  # Inline dependency injection
):
    """
    Retrieves a single package by its UUID.
    """
    try:
        # The CRUD layer raises PackageNotFoundError if not found
        return await crud_package.get_by_id(db, package_id)
    except PackageNotFoundError as e:
        # Translate application error (not found) to 404 Not Found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# --- GET /packages/search (Search by Name) ---
@router.get(
    "/search", response_model=List[PackageOut], summary="Search packages by name"
)
async def search_packages_endpoint(
    name: str = Query(
        ..., min_length=1, description="Partial name to search for (case-insensitive)"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db),  # Inline dependency injection
):
    """
    Searches for packages whose names contain the provided search term.
    """
    return await crud_package.search_by_name(db, name=name, skip=skip, limit=limit)


# --- PUT /packages/{package_id} (Update) ---
@router.put(
    "/{package_id}", response_model=PackageOut, summary="Update an existing package"
)
async def update_package_endpoint(
    package_id: UUID,
    package_in: PackageUpdate,
    db: AsyncSession = Depends(get_db),  # Inline dependency injection
):
    """
    Updates the fields of an existing package identified by UUID.
    """
    try:
        return await crud_package.update(db, package_id=package_id, obj_in=package_in)
    except PackageNotFoundError as e:
        # Raised if package to update is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PackageAlreadyExistsError as e:
        # Raised if a name conflict occurs during update
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# --- DELETE /packages/{package_id} (Delete) ---
@router.delete(
    "/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete package by ID",
)
async def delete_package_endpoint(
    package_id: UUID, db: AsyncSession = Depends(get_db)  # Inline dependency injection
):
    """
    Deletes a package identified by UUID.
    """
    try:
        await crud_package.delete(db, package_id=package_id)
        return
    except PackageNotFoundError as e:
        # Raised if package to delete is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

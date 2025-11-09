# app/api/collections.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.crud import collection as crud_collection
from app.schemas.collection import (
    CollectionCreate,
    CollectionUpdate,
    CollectionResponse,
)

router = APIRouter()


@router.post(
    "/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED
)
async def create_collection(
    collection_in: CollectionCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new collection"""
    return await crud_collection.create(db, obj_in=collection_in)


@router.get("/", response_model=List[CollectionResponse])
async def list_collections(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Get all collections"""
    if active_only:
        return await crud_collection.get_active(db, skip=skip, limit=limit)
    return await crud_collection.get_multi(db, skip=skip, limit=limit)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific collection by ID"""
    collection = await crud_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return collection


@router.get("/slug/{slug}", response_model=CollectionResponse)
async def get_collection_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a collection by slug"""
    collection = await crud_collection.get_by_slug(db, slug=slug)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return collection


@router.put("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: int,
    collection_in: CollectionUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a collection"""
    collection = await crud_collection.get(db, id=collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return await crud_collection.update(db, db_obj=collection, obj_in=collection_in)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a collection"""
    collection = await crud_collection.delete(db, id=collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return None

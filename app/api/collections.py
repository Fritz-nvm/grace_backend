from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud.collection import collection as crud_collection
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
    return await crud_collection.create(db=db, obj_in=collection_in)


@router.get("/", response_model=List[CollectionResponse])
async def list_collections(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud_collection.get_all(db=db, skip=skip, limit=limit)


@router.get("/suite/{suite_id}", response_model=List[CollectionResponse])
async def list_collections_by_suite(
    suite_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud_collection.get_by_suite(
        db=db, suite_id=suite_id, skip=skip, limit=limit
    )


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    collection = await crud_collection.get(db=db, collection_id=collection_id)
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
    db_obj = await crud_collection.get(db=db, collection_id=collection_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return await crud_collection.update(db=db, db_obj=db_obj, obj_in=collection_in)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud_collection.delete(db=db, collection_id=collection_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return None

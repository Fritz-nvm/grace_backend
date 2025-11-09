from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.crud import item as crud_item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new item"""
    return await crud_item.create(db, obj_in=item_in)


@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Get all items"""
    if available_only:
        return await crud_item.get_available(db, skip=skip, limit=limit)
    return await crud_item.get_multi(db, skip=skip, limit=limit)


@router.get("/collection/{collection_id}", response_model=List[ItemResponse])
async def list_items_by_collection(
    collection_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all items in a specific collection"""
    return await crud_item.get_by_collection(
        db, collection_id=collection_id, skip=skip, limit=limit
    )


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific item by ID"""
    item = await crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.get("/slug/{slug}", response_model=ItemResponse)
async def get_item_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get an item by slug"""
    item = await crud_item.get_by_slug(db, slug=slug)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, item_in: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an item"""
    item = await crud_item.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return await crud_item.update(db, db_obj=item, obj_in=item_in)


@router.post("/{item_id}/like", response_model=ItemResponse)
async def like_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Increment the like count for an item"""
    item = await crud_item.increment_likes(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an item"""
    item = await crud_item.delete(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return None

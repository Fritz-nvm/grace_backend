from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud.item import item as crud_item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate, db: AsyncSession = Depends(get_db)):
    """Create a new item"""
    return await crud_item.create(db=db, obj_in=item_in)


@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List items (paginated)"""
    return await crud_item.get_all(db=db, skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Get an item by ID"""
    db_obj = await crud_item.get(db=db, item_id=item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_obj


@router.get("/slug/{slug}", response_model=ItemResponse)
async def get_item_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get an item by slug (if implemented)"""
    if not hasattr(crud_item, "get_by_slug"):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="get_by_slug not implemented",
        )
    db_obj = await crud_item.get_by_slug(db=db, slug=slug)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_obj


@router.get("/collection/{collection_id}", response_model=List[ItemResponse])
async def list_items_by_collection(
    collection_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """List items belonging to a collection"""
    return await crud_item.get_by_collection(
        db=db, collection_id=collection_id, skip=skip, limit=limit
    )


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, item_in: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    """Update an item"""
    db_obj = await crud_item.get(db=db, item_id=item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return await crud_item.update(db=db, db_obj=db_obj, obj_in=item_in)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Delete an item"""
    deleted = await crud_item.delete(db=db, item_id=item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return None

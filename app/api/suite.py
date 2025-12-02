# api/suite.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.database import get_db
from app.schemas.suite import Suite, SuiteCreate, SuiteUpdate, SuiteWithCollections
from app.crud.suite import suite as crud_suite

router = APIRouter()


@router.post("/", response_model=Suite)
async def create_suite(suite_in: SuiteCreate, db: AsyncSession = Depends(get_db)):
    """Create a new suite (returns simple suite without collections)"""
    return await crud_suite.create(db=db, obj_in=suite_in)


@router.get("/name/{suite_name}", response_model=SuiteWithCollections)
async def read_suite_by_name(suite_name: str, db: AsyncSession = Depends(get_db)):
    """Get a suite by name with all collections"""
    db_suite = await crud_suite.get_by_name(db, name=suite_name)
    if db_suite is None:
        raise HTTPException(status_code=404, detail="Suite not found")
    return db_suite


@router.get("/", response_model=List[Suite])
async def read_suites(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Get all suites (simple list without collections)"""
    suites = await crud_suite.get_all(db, skip=skip, limit=limit)
    return suites


@router.get("/with-collections/", response_model=List[SuiteWithCollections])
async def read_suites_with_collections(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Get all suites with collections (use sparingly - can be heavy)"""
    suites = await crud_suite.get_all_with_collections(db, skip=skip, limit=limit)
    return suites


@router.put("/{suite_id}", response_model=Suite)
async def update_suite(
    suite_id: UUID, suite_in: SuiteUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a suite (returns simple suite without collections)"""
    db_suite = await crud_suite.get(db, suite_id=suite_id)
    if db_suite is None:
        raise HTTPException(status_code=404, detail="Suite not found")
    return await crud_suite.update(db=db, db_obj=db_suite, obj_in=suite_in)


@router.delete("/{suite_id}", response_model=Suite)
async def delete_suite(suite_id: UUID, db: AsyncSession = Depends(get_db)):
    """Delete a suite (returns simple suite without collections)"""
    db_suite = await crud_suite.delete(db, suite_id=suite_id)
    if db_suite is None:
        raise HTTPException(status_code=404, detail="Suite not found")
    return db_suite

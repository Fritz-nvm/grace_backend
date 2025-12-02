# app/api/endpoints/testimonials.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud.testimonial import (
    testimonial,
    TestimonialNotFoundError,
    TestimonialAlreadyExistsError,
)
from app.schemas.testimonial import (
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialResponse,
    TestimonialList,
)

router = APIRouter()


@router.post(
    "/",
    response_model=TestimonialResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new testimonial",
)
async def create_testimonial(
    testimonial_in: TestimonialCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new testimonial.

    - **client_name**: Full name of the client (must be unique)
    - **review_text**: Testimonial content (optional, min 10 chars if provided)
    - **rating**: Rating from 0 to 5 stars
    - **display_order**: Sorting order for display
    """
    try:
        return await testimonial.create(db=db, obj_in=testimonial_in)
    except TestimonialAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get(
    "/", response_model=List[TestimonialResponse], summary="Get all testimonials"
)
async def read_testimonials(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Maximum records to return"),
    order_by: str = Query("display_order", description="Sort field (- for descending)"),
    search: Optional[str] = Query(
        None, description="Search in client name or review text"
    ),
    min_rating: Optional[int] = Query(None, ge=0, le=5, description="Minimum rating"),
    max_rating: Optional[int] = Query(None, ge=0, le=5, description="Maximum rating"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get all testimonials with optional filtering and sorting.

    - **skip**: Pagination offset
    - **limit**: Maximum items per page (max 200)
    - **order_by**: Sort by field (e.g., "rating", "-created_at", "display_order")
    - **search**: Search in client name or review text
    - **min_rating**: Filter by minimum rating (0-5)
    - **max_rating**: Filter by maximum rating (0-5)
    """
    try:
        if search:
            # Use search method
            testimonials = await testimonial.search(
                db=db, query=search, skip=skip, limit=limit
            )
        elif min_rating is not None or max_rating is not None:
            # Use rating filter
            min_r = min_rating or 0
            max_r = max_rating or 5
            testimonials = await testimonial.get_by_rating(
                db=db, min_rating=min_r, max_rating=max_r, skip=skip, limit=limit
            )
        else:
            # Get all with ordering
            testimonials = await testimonial.get_all(
                db=db, skip=skip, limit=limit, order_by=order_by
            )
        return testimonials
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get(
    "/{testimonial_id}",
    response_model=TestimonialResponse,
    summary="Get a testimonial by ID",
)
async def read_testimonial(testimonial_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a specific testimonial by its UUID.
    """
    try:
        return await testimonial.get_by_id(db=db, testimonial_id=testimonial_id)
    except TestimonialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get(
    "/client/{client_name}",
    response_model=TestimonialResponse,
    summary="Get a testimonial by client name",
)
async def read_testimonial_by_client_name(
    client_name: str, db: AsyncSession = Depends(get_db)
):
    """
    Get a testimonial by client name (case-insensitive).
    """
    try:
        testimonial_obj = await testimonial.get_by_client_name(
            db=db, client_name=client_name
        )
        if not testimonial_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Testimonial for client '{client_name}' not found.",
            )
        return testimonial_obj
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.put(
    "/{testimonial_id}",
    response_model=TestimonialResponse,
    summary="Update a testimonial",
)
async def update_testimonial(
    testimonial_id: UUID,
    testimonial_in: TestimonialUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a testimonial.

    - All fields are optional
    - Client name must remain unique
    """
    try:
        return await testimonial.update(
            db=db, testimonial_id=testimonial_id, obj_in=testimonial_in
        )
    except TestimonialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TestimonialAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.delete(
    "/{testimonial_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a testimonial",
)
async def delete_testimonial(testimonial_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete a testimonial by ID.

    Returns 204 No Content on success.
    """
    try:
        await testimonial.delete(db=db, testimonial_id=testimonial_id)
    except TestimonialNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get("/stats/count", summary="Get testimonial count")
async def get_testimonial_count(db: AsyncSession = Depends(get_db)):
    """
    Get total number of testimonials.
    """
    try:
        count = await testimonial.get_count(db=db)
        return {"total_testimonials": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )

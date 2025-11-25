from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import collections, items
from app.admin import setup_admin
from sqlalchemy.ext.asyncio import create_async_engine

# Assuming you have a Base class for ORM models
from app.models import Collection, Item

# --- Database Setup ---
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:superuser@localhost:5433/grace"
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
# ----------------------

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware for API endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    collections.router,
    prefix=f"{settings.API_V1_STR}/collections",
    tags=["collections"],
)
app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])


# --- Admin Setup and Mount ---
# Pass the engine and a dictionary of your models to the setup function
admin_app = setup_admin(
    engine=async_engine, models={"Collection": Collection, "Item": Item}
)

# Mount the created admin application (which is the callable Starlette app)
app.mount("/admin", admin_app, name="admin")
# -----------------------------


@app.get("/")
async def root():
    return {"message": "Clothing Brand API", "docs": "/docs", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

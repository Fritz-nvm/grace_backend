from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.api import collections, items, suite
from app.admin import admin, setup_admin_views

from sqlalchemy.ext.asyncio import create_async_engine
import os

load_dotenv()


ASYNC_DATABASE_URL = os.getenv("DATABASE_URL")
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Session middleware for admin authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "change-this-in-production-12345"),
    session_cookie="admin_session",
    max_age=3600,  # 1 hour session
)


# CORS middleware for API endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (for admin images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup admin views
setup_admin_views(admin)

# Mount admin to app
admin.mount_to(app)


app.include_router(
    suite.router, prefix=f"{settings.API_V1_STR}/suites", tags=["suites"]
)

app.include_router(
    collections.router,
    prefix=f"{settings.API_V1_STR}/collections",
    tags=["collections"],
)

app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])


@app.get("/")
async def root():
    return {"message": "Clothing Brand API", "docs": "/docs", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

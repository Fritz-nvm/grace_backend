import sys
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from app.config import settings

try:
    # SQLAlchemy >= 2.0
    from sqlalchemy.ext.asyncio import async_sessionmaker
except ImportError:
    # SQLAlchemy < 2.0
    try:
        from sqlalchemy.ext.asyncio import async_session_maker as async_sessionmaker
    except ImportError:

        def async_sessionmaker(*args, **kwargs):
            from sqlalchemy.ext.asyncio import AsyncSession
            from sqlalchemy.orm import sessionmaker

            return sessionmaker(*args, class_=AsyncSession, **kwargs)


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True if settings.ENVIRONMENT == "development" else False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

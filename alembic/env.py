# alembic/env.py

from logging.config import fileConfig
import sys
import os

from sqlalchemy import pool
from app.models import collection, item
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base
from app.config import (
    get_settings,
)


config = context.config

# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Set the target_metadata to your Base.metadata
target_metadata = Base.metadata

# alembic/env.py (Add this line after target_metadata = Base.metadata)
print("Registered table names:", target_metadata.tables.keys())

# Load the DATABASE_URL from application settings
DATABASE_URL = get_settings().DATABASE_URL


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use the loaded URL for offline mode
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    import asyncio

    async def run_async_migrations():
        async with connectable.connect() as connection:

            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

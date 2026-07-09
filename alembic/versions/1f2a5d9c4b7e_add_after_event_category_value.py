"""add after event category value

Revision ID: 1f2a5d9c4b7e
Revises: 7b6c3d8f0e21
Create Date: 2026-07-09 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f2a5d9c4b7e"
down_revision: Union[str, None] = "7b6c3d8f0e21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE categoryenum ADD VALUE IF NOT EXISTS 'after event'")


def downgrade() -> None:
    # PostgreSQL enum values cannot be removed safely with a simple downgrade.
    pass

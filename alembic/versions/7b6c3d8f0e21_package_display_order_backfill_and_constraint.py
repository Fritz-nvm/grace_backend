"""backfill invalid package display order and enforce nonnegative values

Revision ID: 7b6c3d8f0e21
Revises: e66ebb7d4f52
Create Date: 2026-07-08 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "7b6c3d8f0e21"
down_revision: Union[str, None] = "e66ebb7d4f52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("UPDATE packages SET display_order = 0 WHERE display_order < 0"))
    op.create_check_constraint(
        "ck_packages_display_order_nonnegative",
        "packages",
        "display_order >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_packages_display_order_nonnegative",
        "packages",
        type_="check",
    )

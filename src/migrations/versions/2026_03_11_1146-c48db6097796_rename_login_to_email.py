"""rename login to email

Revision ID: c48db6097796
Revises: 76f436008ba6
Create Date: 2026-03-11 11:46:17.353017

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = "c48db6097796"
down_revision: Union[str, None] = "76f436008ba6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("users", sa.Column("email", sa.String(length=200), nullable=False))
    op.drop_column("users", "login")


def downgrade() -> None:

    op.add_column(
        "users",
        sa.Column("login", sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    )
    op.drop_column("users", "email")


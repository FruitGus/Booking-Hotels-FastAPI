"""unique email = True

Revision ID: 2a6de8893cc4
Revises: c48db6097796
Create Date: 2026-03-11 11:50:57.817043

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a6de8893cc4"
down_revision: Union[str, None] = "c48db6097796"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:

    op.drop_constraint(None, "users", type_="unique")


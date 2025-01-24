"""v1

Revision ID: bc5c7a50f691
Revises: ab9d57484fe2
Create Date: 2025-01-24 09:37:20.327186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc5c7a50f691'
down_revision: Union[str, None] = 'ab9d57484fe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

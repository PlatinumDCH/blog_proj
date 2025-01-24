"""create tables

Revision ID: ab9d57484fe2
Revises: 0a70fae55bcf
Create Date: 2025-01-24 09:34:53.661529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab9d57484fe2'
down_revision: Union[str, None] = '0a70fae55bcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

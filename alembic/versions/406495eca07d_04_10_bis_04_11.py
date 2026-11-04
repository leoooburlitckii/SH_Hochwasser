""" 04.10 bis 04.11

Revision ID: 406495eca07d
Revises: 60127efda195
Create Date: 2026-11-04 22:48:20.962033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '406495eca07d'
down_revision: Union[str, Sequence[str], None] = '60127efda195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

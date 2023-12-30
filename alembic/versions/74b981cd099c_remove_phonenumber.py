"""remove phonenumber

Revision ID: 74b981cd099c
Revises: a44d09dd07ce
Create Date: 2023-12-30 11:21:33.819112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74b981cd099c'
down_revision: Union[str, None] = 'a44d09dd07ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'phone_number')
    pass


def downgrade() -> None:
    op.add_column("users", sa.Column('phone_number', sa.String(length=20), nullable=True))
    pass

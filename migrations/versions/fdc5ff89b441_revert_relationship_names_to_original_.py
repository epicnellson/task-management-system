"""Revert relationship names to original design

Revision ID: fdc5ff89b441
Revises: 2df81da8b3ac
Create Date: 2025-06-10 01:32:08.339115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdc5ff89b441'
down_revision = '2df81da8b3ac'
branch_labels = None
depends_on = None


def upgrade():
    # No changes to password_hash column; only relationship changes were intended.
    pass


def downgrade():
    # No changes to password_hash column; only relationship changes were intended.
    pass

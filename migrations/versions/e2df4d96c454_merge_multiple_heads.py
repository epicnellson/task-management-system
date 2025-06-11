"""merge multiple heads

Revision ID: e2df4d96c454
Revises: 4b1d5f6979ef, bdebd89e857c
Create Date: 2025-06-10 01:21:44.594592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2df4d96c454'
down_revision = ('4b1d5f6979ef', 'bdebd89e857c')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

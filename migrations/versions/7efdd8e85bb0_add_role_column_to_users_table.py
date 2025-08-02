"""Add role column to users table

Revision ID: 7efdd8e85bb0
Revises: a05e9709e3ef
Create Date: 2025-08-02 02:04:16.556426

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7efdd8e85bb0'
down_revision = 'a05e9709e3ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('role', sa.String(length=32), nullable=False, server_default='user'))

def downgrade():
    op.drop_column('users', 'role')


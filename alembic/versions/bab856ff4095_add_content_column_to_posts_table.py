"""add content column to posts table

Revision ID: bab856ff4095
Revises: 9f2c853d7392
Create Date: 2022-03-05 14:42:23.367259

"""
from fastapi import FastAPI
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bab856ff4095'
down_revision = '9f2c853d7392'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

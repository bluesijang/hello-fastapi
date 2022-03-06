"""create posts table

Revision ID: 9f2c853d7392
Revises: 
Create Date: 2022-03-05 14:32:44.145116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2c853d7392'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.INTEGER, nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    


def downgrade():
    op.drop_table('posts')
    

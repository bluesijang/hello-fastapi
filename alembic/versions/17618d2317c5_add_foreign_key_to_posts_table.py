"""add foreign-key to posts table

Revision ID: 17618d2317c5
Revises: 2fd865ca95e6
Create Date: 2022-03-05 14:54:43.481829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17618d2317c5'
down_revision = '2fd865ca95e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass


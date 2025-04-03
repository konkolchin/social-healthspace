"""add community to posts

Revision ID: 30642e355924
Revises: 30642e355923
Create Date: 2024-04-02 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '30642e355924'
down_revision = '30642e355923'
branch_labels = None
depends_on = None

def upgrade():
    # Add community_id column to posts table
    op.add_column('posts', sa.Column('community_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_post_community_id',
        'posts', 'communities',
        ['community_id'], ['id']
    )

def downgrade():
    op.drop_constraint('fk_post_community_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'community_id')

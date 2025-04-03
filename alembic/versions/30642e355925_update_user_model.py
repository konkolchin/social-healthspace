"""update user model

Revision ID: 30642e355925
Revises: 30642e355924
Create Date: 2024-04-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '30642e355925'
down_revision = '30642e355924'
branch_labels = None
depends_on = None

def upgrade():
    # Drop old columns
    op.drop_column('users', 'username')
    op.drop_column('users', 'full_name')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'is_superuser')
    
    # Add new name column
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))

def downgrade():
    # Drop new column
    op.drop_column('users', 'name')
    
    # Add back old columns
    op.add_column('users', sa.Column('username', sa.String(), nullable=False))
    op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('bio', sa.String(), nullable=True))
    op.add_column('users', sa.Column('avatar_url', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    
    # Create unique index for username
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True) 
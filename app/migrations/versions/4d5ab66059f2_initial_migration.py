"""Initial migration

Revision ID: 4d5ab66059f2
Revises: 
Create Date: 2025-02-17 12:03:01.925774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d5ab66059f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
    )

    # Create 'books' table
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('isbn', sa.String, unique=True, nullable=False),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('createdAt', sa.TIMESTAMP, nullable=False),
        sa.Column('updateAt', sa.TIMESTAMP, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )


def downgrade() -> None:
    # Drop 'books' table first due to foreign key dependency
    op.drop_table('books')
    # Drop 'users' table
    op.drop_table('users')

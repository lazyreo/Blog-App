"""create initial users and blogs tables

Revision ID: 0001_create_initial_tables
Revises: 
Create Date: 2026-06-18 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_initial_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            'username',
            sa.String(length=15),
            nullable=False,
            index=True,
            unique=True
        ),

        sa.Column(
            'email',
            sa.String(length=255),
            nullable=False,
            index=True,
            unique=True
        ),

        sa.Column(
            'password_hash',
            sa.String(length=255),
            nullable=False
        ),
        
        sa.Column(
            'password_hash',
            sa.String(length=255),
            nullable=False
        ),
        
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False
        ),
    )

    op.create_table(
        'blogs',

        sa.Column(
            'id',
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            'user_id',
            sa.Integer(),
            sa.ForeignKey(
                'users.id'),
            unique=True,
            nullable=False
        ),

        sa.Column(
            'title',
            sa.String(length=255),
            nullable=False
        ),

        sa.Column(
            'slug',
            sa.String(length=255),
            nullable=False,
            index=True,
            unique=True
        ),

        sa.Column(
            'content',
            sa.Text(),
            nullable=True
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False
        ),
        
    )


def downgrade():
    op.drop_table('blogs')
    op.drop_table('users')

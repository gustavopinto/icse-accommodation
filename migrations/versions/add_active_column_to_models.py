"""add active column for soft delete

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-03-01

"""
from alembic import op
import sqlalchemy as sa


revision = "e6f7a8b9c0d1"
down_revision = "d5e6f7a8b9c0"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("accommodation_requests", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true())
        )
    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true())
        )


def downgrade():
    with op.batch_alter_table("accommodation_requests", schema=None) as batch_op:
        batch_op.drop_column("active")
    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.drop_column("active")

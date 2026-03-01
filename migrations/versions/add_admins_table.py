"""add admins table

Revision ID: add_admins_01
Revises: 15dce7787334
Create Date: 2026-03-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c4d5e6f7a8b9"
down_revision = "15dce7787334"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "admins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_admins_username"), ["username"], unique=True)


def downgrade():
    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_admins_username"))
    op.drop_table("admins")

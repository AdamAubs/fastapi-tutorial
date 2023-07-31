"""add user table

Revision ID: dd12a6c8e048
Revises: e09329df782b
Create Date: 2023-07-30 06:03:35.753893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dd12a6c8e048"
down_revision = "e09329df782b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass

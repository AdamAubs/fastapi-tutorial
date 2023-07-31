"""add last few columns to posts table

Revision ID: c6c85a28a615
Revises: 2b820b4051b0
Create Date: 2023-07-30 06:42:32.900424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c6c85a28a615"
down_revision = "2b820b4051b0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass

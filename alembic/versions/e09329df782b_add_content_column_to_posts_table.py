"""add content column to posts table

Revision ID: e09329df782b
Revises: be6140400bc5
Create Date: 2023-07-30 05:46:30.912734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e09329df782b"
down_revision = "be6140400bc5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass

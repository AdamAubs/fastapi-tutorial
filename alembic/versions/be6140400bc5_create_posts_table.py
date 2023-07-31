"""create posts table

Revision ID: be6140400bc5
Revises: 
Create Date: 2023-07-30 05:15:57.426265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "be6140400bc5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

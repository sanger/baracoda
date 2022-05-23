"""add child barcode counter table


Revision ID: e505f2e15499
Revises: e501839465f6
Create Date: 2022-04-06 14:58:18.990940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e505f2e15499"
down_revision = "e501839465f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "child_barcode_counter",
        # ID
        sa.Column("barcode", sa.String(50), nullable=False),
        sa.Column("child_count", sa.Integer(), nullable=True),
        # Created_at
        sa.PrimaryKeyConstraint("barcode"),
    )


def downgrade():
    op.drop_table("child_barcode_counter")
    # ### end Alembic commands ###

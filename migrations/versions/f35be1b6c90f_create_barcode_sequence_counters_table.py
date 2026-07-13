"""create barcode sequence counters table

Revision ID: f35be1b6c90f
Revises: 4f525be49d95
Create Date: 2026-06-19 12:09:40.040102

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f35be1b6c90f"
down_revision = "4f525be49d95"
branch_labels = None
depends_on = None


def upgrade():
    # Create the counter table to replace PostgreSQL sequences
    op.create_table(
        "barcode_sequence_counters",
        sa.Column("sequence_name", sa.String(50), nullable=False),
        sa.Column("current_value", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("sequence_name"),
    )

    # IMPORTANT: Counter values must be seeded manually during deployment
    # from the current PostgreSQL sequence values in production.
    # DO NOT auto-populate - this must be done carefully to avoid duplicate barcodes.
    # Set each sequence_name to (current_postgres_value + 1) to continue numbering.
    # Example: if SQP is currently at 9000 in PostgreSQL, set it to 9001 here.
    # This should be done via a separate deployment script before going live.


def downgrade():
    op.drop_table("barcode_sequence_counters")

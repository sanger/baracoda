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

    # Initialize all 6 sequences with their start values
    op.execute(
        """
        INSERT INTO barcode_sequence_counters (sequence_name, current_value)
        VALUES
            ('heron', 200000),
            ('ht', 111111),
            ('sqp', 1),
            ('csm', 111111),
            ('pam', 111111),
            ('rvi', 111111)
    """
    )


def downgrade():
    op.drop_table("barcode_sequence_counters")

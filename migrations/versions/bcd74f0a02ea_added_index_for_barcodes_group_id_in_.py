"""Added index for barcodes_group_id in barcodes tables

Revision ID: bcd74f0a02ea
Revises: e47fde01cc62
Create Date: 2022-10-11 15:23:43.608690

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "bcd74f0a02ea"
down_revision = "e47fde01cc62"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("barcodes_group_id_index", "barcodes", ["barcodes_group_id"])


def downgrade():
    op.drop_index("barcodes_group_id_index", table_name="barcodes")

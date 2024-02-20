"""Add sqp sequence

Revision ID: e501839465f6
Revises: bc442d63d7d3
Create Date: 2022-04-04 14:38:35.746245

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "e501839465f6"
down_revision = "bc442d63d7d3"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE sqp START 1;")


def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS sqp;")

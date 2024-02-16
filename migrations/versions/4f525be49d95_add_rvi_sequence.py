"""Add rvi sequence

Revision ID: 4f525be49d95
Revises: db39b037a71d
Create Date: 2024-02-16 10:08:39.833576

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4f525be49d95"
down_revision = "db39b037a71d"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE rvi START 111111;")


def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS rvi;")

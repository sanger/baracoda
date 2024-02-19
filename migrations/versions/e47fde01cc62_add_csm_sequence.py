"""add csm sequence

Revision ID: e47fde01cc62
Revises: e505f2e15499
Create Date: 2022-10-06 16:24:05.695978

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "e47fde01cc62"
down_revision = "e505f2e15499"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE csm START 111111;")


def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS csm;")

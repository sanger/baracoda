"""add_pam_sequence

Revision ID: db39b037a71d
Revises: bcd74f0a02ea
Create Date: 2022-10-21 14:45:22.805527

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "db39b037a71d"
down_revision = "bcd74f0a02ea"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE pam START 111111;")


def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS pam;")

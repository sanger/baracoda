"""Add SEQ_DNAPLATE sequence

Revision ID: c742377339a6
Revises: bc442d63d7d3
Create Date: 2022-03-23 15:23:22.964360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c742377339a6"
down_revision = "bc442d63d7d3"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE SEQ_DNAPLATE START 1;")


def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS SEQ_DNAPLATE;")

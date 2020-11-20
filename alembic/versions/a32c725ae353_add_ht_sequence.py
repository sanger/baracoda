"""add ht sequence.

Revision ID: a32c725ae353
Revises: 0898a303eb2a
Create Date: 2020-11-16 16:41:01.995768

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a32c725ae353"
down_revision = "0898a303eb2a"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE SEQUENCE ht START 111111;")

def downgrade():
    op.execute("DROP SEQUENCE IF EXISTS ht;")

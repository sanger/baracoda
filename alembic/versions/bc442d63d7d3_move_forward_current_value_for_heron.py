"""Move forward current value for heron

Revision ID: bc442d63d7d3
Revises: a32c725ae353
Create Date: 2021-10-13 14:07:48.425000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "bc442d63d7d3"
down_revision = "a32c725ae353"
branch_labels = None
depends_on = None


def upgrade():
    # Last value in database is 2564197, we want to move forward past this value
    op.execute("ALTER SEQUENCE serial RESTART WITH 2564300;")


def downgrade():
    # Actual value in Baracoda is 2156143, but if we rollback we can leave a bit of space
    # Please retrieve the last actual value and edit if you plan to downgrade
    pass

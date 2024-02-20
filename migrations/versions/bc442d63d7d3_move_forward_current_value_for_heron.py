"""Move forward current value for heron

Revision ID: bc442d63d7d3
Revises: a32c725ae353
Create Date: 2021-10-13 14:07:48.425000

"""

from alembic import op
import os

# revision identifiers, used by Alembic.
revision = "bc442d63d7d3"
down_revision = "a32c725ae353"
branch_labels = None
depends_on = None


def __DANGER_restart_sequence_with(value):
    if os.environ.get("CONFIRM_HERON_SEQUENCE_RESTART") is None:
        description = (
            "'This migration is potentially destructive. Update the value for RESTART WITH"
            "to a known unused value and set the environment variable "
            "CONFIRM_HERON_SEQUENCE_RESTART to confirm you want to apply this migration.'"
        )
        raise ValueError(description)
    # Last value in database is 2564197, we want to move forward past this value
    op.execute(f"ALTER SEQUENCE heron RESTART WITH { value };")


def upgrade():
    # Last value in database is 2564197, we want to move forward past this value
    __DANGER_restart_sequence_with(2564300)


def downgrade():
    # Actual value in Baracoda is 2156143, but if we rollback we can leave a bit of space
    # Please retrieve a sensible value and edit if you plan to downgrade
    description = (
        "\nPlease substitute this exception with a line in python like: \n"
        "__DANGER_restart_sequence_with(<newvalue>)\n"
        "where <newvalue> is a SAFE value you estimate.\n"
    )
    raise Exception(description)

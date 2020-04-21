from baracoda import create_app

import pytest
def test_exit_wrong_config():

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            create_app({})
    assert pytest_wrapped_e.type == SystemExit

def test_creates_app_right_config():
    assert create_app({
            "DB_HOST":"localhost",
            "DB_PORT":5432,
            "DB_USER":"emr",
            "DB_PASSWORD":"emr",
            "DB_DBNAME":"mydb",
            "SEQUENCE_NAME":"heron",
            "SEQUENCE_START":1
        })

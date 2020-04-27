from baracoda import create_app


def test_creates_app_right_config():
    assert create_app(
        {
            "DB_HOST": "localhost",
            "DB_PORT": 5432,
            "DB_USER": "test",
            "DB_PASSWORD": "test",
            "DB_DBNAME": "mydb",
            "SEQUENCE_NAME": "heron",
            "SEQUENCE_START": 1,
        }
    )

import pytest

from orm.database import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope="function")
def sqlalchemy_mock_config():
    return [("user_account", [
        {
            "id": 1,
            "email": "test@test.com",
            "hashed_password": "12345",
        },
    ])]

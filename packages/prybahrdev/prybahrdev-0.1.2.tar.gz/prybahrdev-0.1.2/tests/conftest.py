import pytest


@pytest.fixture(scope="module")
def eg_dev_fixture():
    return 'this is my eg-dev-fixture'

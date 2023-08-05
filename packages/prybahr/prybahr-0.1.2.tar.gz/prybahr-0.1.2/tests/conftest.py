import pytest


@pytest.fixture(scope="module")
def eg_fixture():
    return 'this is my eg-fixture'

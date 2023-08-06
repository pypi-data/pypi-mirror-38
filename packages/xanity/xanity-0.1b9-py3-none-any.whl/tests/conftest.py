## pytest config
import difflib
import pytest

@pytest.fixture(scope="session")
def test_temp_path(tmp_path_factory):
	here = tmp_path_factory.mktemp('test_here')
	other = tmp_path_factory.mktemp('test_other')
	return [here, other]

@pytest.fixture(scope="session")
def test_proj_here(test_temp_path):
    return ('xanity_test_proj_here', test_temp_path[0])

@pytest.fixture(scope="session")
def test_proj_other(test_temp_path):
    return ('xanity_test_proj_other', test_temp_path[1])

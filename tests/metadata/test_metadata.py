import mlbriefcase
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_metadata(test_subdir):
    ws = mlbriefcase.Briefcase()

    metadata = ws['query1'].metadata
    assert isinstance(metadata, dict)

    assert metadata['a'] == 1
    assert metadata['tag'] == 'datasource'

    assert metadata['b'] == [1, 2]

def test_get_all(test_subdir):
    ws = mlbriefcase.Briefcase()

    all = ws.get_all()

    assert len(all) == 1
    assert all[0].name == 'query1'
import mlbriefcase
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_can_load_empty(test_subdir):
    ws = mlbriefcase.Briefcase()
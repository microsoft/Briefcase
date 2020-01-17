import mlbriefcase
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_no_immediate_properties(test_subdir):
    ws = mlbriefcase.Briefcase()
    client = ws['face_test'].get_client() 
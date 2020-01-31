import mlbriefcase
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_dont_infinite_recurse_if_cred_not_found(test_subdir):
    with pytest.raises(mlbriefcase.base.KeyNotFoundException, match=r".*myserviceprincipal.*EnvironmentCredentialProvider.*"):
        ws = mlbriefcase.Briefcase()
        client = ws['face_test'].get_client() 
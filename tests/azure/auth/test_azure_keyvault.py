import mlbriefcase
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# @pytest.mark.skipif(os.environ.get('myserviceprincipal1') is None,
                    # reason='Environment variable myserviceprincipal1 must be set to service principals secret')
def test_azure_keyvault(test_subdir):

    ws = mlbriefcase.Briefcase()

    svc1 = ws['kv1']
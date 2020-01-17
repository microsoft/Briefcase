import mlbriefcase
import pytest
import os
import pandas as pd


@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.mark.skipif(os.environ.get('myserviceprincipal1') is None,
                    reason='Environment variable myserviceprincipal1 must be set to service principals secret')
def test_azure_storage_url(test_subdir):
    ws = mlbriefcase.Briefcase()

    url = ws['workspacetest1'].get_url()
    df = pd.read_csv(url, sep='\t')

    assert (df.columns == ['a', 'b', 'c']).all()
    assert df.shape == (2, 3)

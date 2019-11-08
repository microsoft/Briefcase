import pyworkspace
import keyring
import os
import pytest

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_Workspace_can_load(test_subdir):
    ws = pyworkspace.Workspace()

def test_Workspace_can_find_AzureStorage(test_subdir):
    ws = pyworkspace.Workspace()

    assert 0 < len(ws.get_all_of_type(pyworkspace.azure.AzureStorage))

def test_Workspace_indexing(test_subdir):
    ws = pyworkspace.Workspace()

    assert ws['credentials/myvault1'] is not None
    assert ws['credentials.myvault1'] is not None
    assert ws['myvault1'] is not None
    assert ws['myvault2'] is None

class MockKeyVaultSecret():
    def __init__(self, value):
        self.value = value

class MockKeyVault():
     def get_secret(self, dnsname, key, secret_version):
         return MockKeyVaultSecret('123')

def test_Credential_Resolution(test_subdir):
    ws = pyworkspace.Workspace()

    # make sure we don't call out to keyvault in tests
    for keyvault in ws.get_all_of_type(pyworkspace.azure.AzureKeyVault):
        keyvault.set_client(MockKeyVault())

    # mock keyvault appends 123 at the end
    # explicit credential store reference
    assert '123' == ws['myblobsource1'].get_secret() 
    # just enumerate all credential stores
    # assert '123' == ws['myblobsource2'].get_secret() 

def test_e2e_storage_pandas(test_subdir):
    ws = pyworkspace.Workspace()

    df = ws['csv1'].to_pandas_dataframe()
    assert (df.columns == ['a', 'b', 'c']).all()
    assert df.shape == (2, 3)

def test_cog_service_keyring(test_subdir):
    ws = pyworkspace.Workspace()

    keyring.set_password('pyworkspace', 'anom1', 'abc123')

    svc1 = ws['anom1']
    
    assert svc1.url == 'https://foo.bar'
    assert svc1.get_secret() == 'abc123'
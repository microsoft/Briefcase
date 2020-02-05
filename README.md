[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20Python?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=1&branchName=master)
[![PyPI version](https://badge.fury.io/py/mlbriefcase.svg)](https://badge.fury.io/py/mlbriefcase)

# Contributing
This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

# What is this?
This projects provides an abstraction layer between secrets and services by externalizing the configuration using yaml.
In constrast to other config libraries the library returns fully-configured and authenticated client SDK objects for services.
Secrets can be fetched from a number of sources.
It's expected that the briefcase.yaml is stored along side notebooks (e.g. in the root folder of a git repository). 

## Goals
* Simplify authentication
* Enable resource sharing between Notebooks and team members
* Improve service specific SDK discoverability

## Example: Azure Blob and Environment Variable
Accessing private blobs is usually performed using SAS tokens or by sharing account keys.

```bash
pip install mlbriefcase
```

Create briefcase.yaml
```yaml
azure:
    storage:
        blob:
            -name: blob1
             url: https://myblob123.blob.core.windows.net/test/test.csv
```

```bash
# use Azure Storage Account key
export blob1=KwY...8w==
```

```python
import mlbriefcase
import pandas as pd

# searches for briefcase.yaml in current directory and all parent directories
briefcase = mlbriefcase.Briefcase()

# let's get the resource by name
blob = briefcase['blob1']

# Performs
# - probe credential providers (e.g. environment variable, dotenv, ...) to find storage account key
# - create Azure Storage SDK object (available through blob.get_client())
# - generated authenticated url using SAS token
url = blob.get_url()  

df = pd.read_csv(url, sep='\t')
``` 

## Example: Azure Cognitive Vision Service and .env file
This example demonstrate how to get the Azure Cognitive Vision service client.

Create briefcase.yaml
```yaml
azure:
  cognitiveservice:
    vision:
      - name: vision1
```

```.env
vision1=<Insert Cog Service Key>
```

```python
import mlbriefcase

# searches for briefcase.yaml in current directory and all parent directories
briefcase = mlbriefcase.Briefcase()

# Performs
# - probe credential providers (e.g. environment variable, dotenv, ...) to find cognitive service key
# - initialize the Cognitive Service Vision SDK object
vision = briefcase['vision1'].get_client()

vision.detect... # TODO
```

## Rules of the Game
1. briefcase.yaml is searched in the current directory and if not found recursed until the root directory.
2. The name of a service (e.g. vision1) is used as the key name for the corresponding secret. The key can be customized (see [Remapping Keys](#Remapping-Keys)).
3. Credential providers are probed for keys in order
 - [Jupyter Lab Credentials](https://towardsdatascience.com/the-jupyterlab-credential-store-9cc3a0b9356)
 - [Python Keyring](https://pypi.org/project/keyring)
 - Environment variables
 - [.env](https://github.com/theskumar/python-dotenv) files
 - All credential providers defined in the briefcase.yaml
 Behavior can be customized - see [Specific credential provider](#Specific-credential-provider)
4. Any other required service property not found in the yaml is searched for in credential providers (e.g. one might not want to share the endpoint for a keyvault) using name.property (or name_property for environment variables)

# Features
## Remapping Keys
In the example below the Cognitive Service Vision token is searched using VISION_KEY. Since the url is not specified and remapped it's search using VISION_URL.

```yaml
azure:
    cognitiveservice:
        vision:
         - name: vision1
           secret:
            key: VISION_KEY
           url:
            key: VISION_URL
```

## Specific credential provider
As mentioned earlier which credential provider is used for lookup can be customized using the credentialprovider property.

```yaml
azure:
    keyvault:
     - name: kv1
       dnsname: https://myvault.vault.azure.net/
    
    storage:
        account:
         - name: blob1
           accountname: test1
           credentialprovider: kv1
        account:
         - name: blob2
           accountname: test2
           credentialprovider: env

python:
    env: 
     - name: env
```

## IntelliSense in VSCode
To ease authoring we provide a JSON schema used by [VS Code yaml plugin](https://github.com/redhat-developer/vscode-yaml) and enables IntelliSense in VS Code.

## Authentication
The default order for credential provider resolution:
1. Jupyter Lab Credential Provider
2. Python KeyRing
3. Environment variables
4. .env fiels
5. Any declared credential provider resource found in briefcase.yaml

For Azure resources the following authentication methods are supported
1. Service Principal
2. Azure Device Login
3. Azure Managed Service identity

# FAQ
## How to get the logging to work on Jupyter?
Add the following cells to your Jupyter notebook (and yes the first cell throws an error, but that seems to be required).

```python
%config Application.log_level='WORKAROUND'
```

```python
import logging
logging.getLogger('briefcase').setLevel(logging.DEBUG)
```

## Python
* Service SDK libraries are imported at time of usage (e.g. resource.get_client())
* If import fails, exception contains the name of the pip package

# Development
Run 

```bash
pip install -e .[test]

cd tests
pytest -s . -k test_sql_alchemy
```

Note: most tests depend on secrets thus you won't be able to run them without setting up your own resources.

## How to add a new resource?
1. Add the resource definition to [JSON schema](mlbriefcase/briefcase-schema.json)
2. The path to the resource is used as the package/class name  (e.g. [azure.cognitiveservice.vision](mlbriefcase/azure/cognitiveservice/vision.py)). Name your resource accordingly.

```yaml
azure:
    cognitiveservice:
        vision:
         - name: vision1
 ```

3. Inherit from Resource
4. Define pip_package variable
5. define get_client_lazy
6. Use self.get_secret() to trigger secret resolution
7. Use self.<your-property> to access any other property required by your resource

## YAML / JSON Schema
To get live updates of JSON schema and validate in VS Code, update the settings to directly reference the JSON schema.
```json
    "yaml.schemas": {
        "file:///mnt/c/work/Workspace/mlbriefcase/briefcase-schema.json": ["briefcase.yaml"]
    }
```

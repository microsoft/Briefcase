
[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20Python?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=1&branchName=master)
Python

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

# What is this? (TODO)
This projects provides an abstraction layer between secrets and services by externalizing the configuration using yaml.
In constrast to other config libraries the library returns fully-configured and authenticated client SDK objects for services.
Secrets can be fetched from a number of sources.
It's expected that the briefcase.yaml is stored along side notebooks (e.g. in the root folder of a git repository). 

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
export blob1=<TODO insert KEY START...>
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
vision1=<TODO Cog Service Key>
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
2. The name of a service (e.g. vision1) is used as the key name for the corresponding secret. The key can be customized (see [Remapping Keys]).
3. Credential providers are probed for keys in order
 - [Jupyter Lab Credentials](TODO)
 - [Python Keyring](TODO)
 - Environment variables
 - [.env](TODO) files
 - All credential providers defined in the briefcase.yaml
 Behavior can be customized - see [Specific credential provider]
3. Any other required service property not found in the yaml is searched for in credential providers (e.g. one might not want to share the endpoint for a keyvault).

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

When developing update the VS Code settings to directly reference the JSON schema.
```json
    "yaml.schemas": {
        "file:///mnt/c/work/Workspace/briefcase-schema.json": ["briefcase.yaml"]
    }
```


TODO: Link to Redhat VS Code plugin
TODO: Upload briefcase-schema.json to json-schema.org

# Open Design decisions
- Should built-in credential providers by predefined (e.g. env, dotenv, ...)
- Should we allow for multiple credential providers?

# Demo
![Demo recording](images/demo1.gif)

## What is happening?

* This scenario shows how to levarage your idenity on [Azure Notebook](https://notebooks.azure.com) to securely access project resources.
* The already created _resources.yaml_ contains all resources our project references. This can be blobs, databases, ... (see full list below). The referenced Azure Storage blob is *not* public, but requires authentication.
* We can authorize our notebook to access Azure resources by hitting the "Azure/Connect to Azure..." button
* Now we can create the Workspace object that helps us manage resources and simplifies credential management
  * When looking up the resource 'workspacetest1' and retrieving the url the credential lookup process is triggered.
  * First credential providers configured in the yaml are probed (none in the example).
  * Second silent credential providers are probed (e.g. environment variables).
  * Third we're falling back Microsoft Managed Service Identity.
  * Since no Azure subscription is referenced in the yaml we enumerate all available.
  * We search all Azure subscriptions for the Azure Storage account 'workspacetest' and retrieve the key.
  * Finally we found the storage account keys and are able to generate a URL with an SAS token
* At this point we can start with the data science work and look at the data using Pandas.
## Authentication

| Type | Python | C# | JavaScript |
|---|:---:|:---:|:---:|
| Azure Device Login | :heavy_check_mark: |  |  |
| Azure Service Principal | :heavy_check_mark: | :heavy_check_mark: |  |
| Azure Managed Service Identity | :heavy_check_mark: |  |  |
| Windows Integrated |  | :heavy_check_mark: |  |
| Environment Variables | :heavy_check_mark: | :heavy_check_mark: |  |
| Python KeyRing | :heavy_check_mark: |  |  |
| JupyterLab Credentials | :heavy_check_mark: |  |  |

For Azure resources the following methods are probed:

1. Azure Managed Service identity (e.g. available in Azure Notebooks)
2. Azure Device Login

# FAQ

## How to get the logging to work on Jupyter?

Add the following cells to your Jupyter notebook (and yes the first cell throws an error, but that seems to be required).

```python
%config Application.log_level='WORKAROUND'
```

```python
import logging
logging.getLogger('workspace').setLevel(logging.DEBUG)
```

# What is it?
_Briefcase_ was created to manage all your authoring time service connection strings and *dataset* references in a *resources.yaml*
usually located at the root of your git repository.
The provided libraries aims to simplify access by automating authentication and natural integration with service specific SDKs.
Futhermore we aim for tooling support (e.g. list storage accounts in VSCode). 

# Features
* Simplify authentication
* Enable resource sharing between Notebooks and team members
* Improve service specific SDK discoverability
* Organize resources using arbitrary hierarchies

## Python

* Service SDK libraries are imported at time of usage (e.g. resource.get_client())
* If import fails, exception contains the name of the pip package

# Development

# YAML / JSON Schema

# Python

cd python
pip install -e .[test]

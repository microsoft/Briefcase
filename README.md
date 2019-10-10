
[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20Python?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=1&branchName=master)
Python

[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20DotNet%20Core?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=3&branchName=master)
.NET Core

[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20DotNet%20Desktop?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=2&branchName=master)
.NET Desktop

[![Build Status](https://dev.azure.com/ossworkspace/Workspace/_apis/build/status/Microsoft.Workspace%20TypeScript?branchName=master)](https://dev.azure.com/ossworkspace/Workspace/_build/latest?definitionId=4&branchName=master)
TypeScript

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
_Workspace_ was created to manage all your authoring time service connection strings and *dataset* references in a *resources.yaml*
usually located at the root of your git repository.
The provided libraries aims to simplify access by automating authentication and natural integration with service specific SDKs.
Futhermore we aim for tooling support (e.g. list storage accounts in VSCode). 

# Features
* Simplify authentication
* Enable resource sharing between Notebooks and team members
* Improve service specific SDK discoverability
* Organize resources using arbitrary hierarchies

# How to get started
Put your resources into *resources.yaml* (see sample below).

In your Python notebook use

```bash
pip install pyworkspace
```

```python
import pyworkspace

ws = pyworkspace.Workspace() # assumes your current directory is some where in your git repository

print(ws['csv1'].get_secret())

# requires 'pip install pandas azureml-dataprep'
df = ws['csv1'].to_pandas_dataframe()
```

In your C# project include [TODO] nuget and use

```C#
var ws = new workspace.Workspace()

ws['csv1'].download()
```

# Examples
## Data Science
Larger projects require multiple notebooks -> share data set specification + authentication between notebooks

## Development (C#)
Within unit tests larger files are used and stored on an Azure Storage account, they can be looked up using this tool.
In general cloud resource is simplified as authentication is performed using the currently logged in user.

# The loooonger story
Some motivation: considering real-life projects multiple personas (e.g. devs, data scientists, data engineers) are collaborating and sometimes roles overlap. Each persona has a set of tools that are tailored toward the role (e.g. VS Code to devs, AzureML Workspace/Azure Databricks for data scientists, ...). Today we use git to at least move source code artifiacts between them, but each toolset/environment has it's own notion of service and data connections (or more broadly resources). 
And that's where this project comes in. We define a common location and semantic in a file assumed to be located in the root of your git repository called *resources.yaml*. One complication in the story are credentials, which we definitely don't want to put into our beloved git repository. 

This project provides a set of tools in multiple languages (Python, JavaScript and C# to start with), which aims to offer parsing, credential and convenience support to the respective language users.

Thus Python users will get easy access functions for data (e.g. from an Azure Storage Blob to a Pandas data frame) vs C# will get download support to enable unit test scenarios.

As we go along we're actively working with toolset owners (e.g. VSCode extensions) to enable support for *resources.yaml*. 

# Development principals
*

## Python
* Service SDK libraries are imported at time of usage (e.g. resource.get_client())


# Development

# Python

cd python
pip install -e .[test]

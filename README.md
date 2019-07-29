
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
pip install -e . 
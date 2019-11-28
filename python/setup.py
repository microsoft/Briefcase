from setuptools import setup, find_packages

from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, '..', 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

setup(name='pyworkspace',
      version='0.1',
      description='Manages your cloud resources across multiple executing environments.',
      url='http://github.com/Microsoft/Workspace',
      author='Markus Cozowicz',
      author_email='marcozo@microsoft.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research'
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      keywords='cloud security resources',
      python_requires='>=3',
      install_requires=['pyyaml', 'python-dotenv'],
      extras_require={
          'test': ['azureml-dataprep[pandas]',
                   'azure-keyvault',
                   'azure-storage-blob',
                   'azure-mgmt-storage',
                   'azure-mgmt-subscription',
                   'boto3',
                   'google-auth',
                   'google-cloud',
                   'google-cloud-language',
                   'google-cloud-vision',
                   'google-cloud-videointelligence',
                   'clarifai',
                   'sqlalchemy',
                   'keyring',
                   'keyrings.alt',  # not recommended for production
                   'secretstorage',
                   'pytest'],
      },
      packages=find_packages())

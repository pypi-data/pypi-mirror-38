# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['decouple_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.7,<2.0', 'python-decouple>=3.1,<4.0']

setup_kwargs = {
    'name': 'python-decouple-aws',
    'version': '0.3.1',
    'description': 'AWS Extensions for Python Decouple',
    'long_description': "Python Decouple AWS\n===================\n\n.. image:: https://img.shields.io/pypi/v/python-decouple-aws.svg\n    :target: https://pypi.python.org/pypi/python-decouple-aws/\n    :alt: Latest PyPI version\n\n\n*Python Decouple AWS* helps you to organize and access sensitive information on AWS Secrets Manager.\n\nIt also makes it easy for you to:\n\n#. Not repeat the boto3 boilerplate code;\n#. Define default values;\n#. Use os.environ as fall back;\n\nSupports Python 3.4+\n\nWhy\n------------\n\n- Single place to save all secrets (AWS Secrets Manager)\n- Keep sensitive information away from code and environments\n- Simpler API to access AWS Secrets Manager (rather than boto3)\n\n\nInstallation\n------------\n::\n\n    pip install python-decouple-aws\n\n\nUsage example 1\n---------------\n::\n\n    #  settings.py\n    from decouple_aws import get_config\n\n    # The package provides a wrapper function that will\n    # fallback to environment variables and fail gracefully\n    # if AWS Secrets Manager is not accessible for whatever\n    # reason.\n    config = get_config('your-project/secret/name', 'ap-southeast-2')\n\n    # Use decouple config like normal\n    MY_EMAIL_USER = config('MY_EMAIL_USER', 'default-user')\n    MY_EMAIL_PASS = config('MY_EMAIL_PASS')\n\n\nUsage example 2\n---------------\n::\n\n    # settings.py\n    from decouple import Config\n    from decouple_aws import RepositoryAwsSecretManager\n\n    # if you would like it to fail if secrets\n    # manager is inaccessible, you can build it manually.\n    # initialise the config with the AWS repository\n    # Pass the repo your secret name and the region\n    repo = RepositoryAwsSecretManager('your-project/secret/name', 'ap-southeast-2')\n    config = Config(repo)\n\n    # Use decouple config like normal\n    MY_SUPER_SECRET_SETTING = config('MY_SUPER_SECRET_SETTING')\n",
    'author': 'Matt Magin',
    'author_email': 'matt.magin@cmv.com.au',
    'url': 'https://github.com/AzMoo/python-decouple-aws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

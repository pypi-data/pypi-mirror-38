# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snakeless_provider_gcloud']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.1,<3.0', 'google-auth>=1.5,<2.0', 'requests>=2.20,<3.0']

entry_points = \
{'snakeless.providers': ['gcloud = snakeless_provider_gcloud:GCloudProvider'],
 'snakeless.schemas': ['gcloud = snakeless_provider_gcloud:GCLOUD_SCHEMA']}

setup_kwargs = {
    'name': 'snakeless-provider-gcloud',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'German Ivanov',
    'author_email': 'germivanov@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

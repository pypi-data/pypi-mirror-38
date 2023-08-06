# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rafi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rafi',
    'version': '0.1.0',
    'description': 'A tiny route dispatcher for Google Cloud Functions.',
    'long_description': None,
    'author': 'Danilo Braband',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['twod']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'twod',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'jnyjny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

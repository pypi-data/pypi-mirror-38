# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['twod']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'twod',
    'version': '0.1.1',
    'description': 'Two Dimensional Geomtric Objects',
    'long_description': None,
    'author': 'jnyjny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'url': 'https://github.com/JnyJny/twod',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

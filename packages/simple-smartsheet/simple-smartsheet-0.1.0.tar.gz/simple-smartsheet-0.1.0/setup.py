# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simple_smartsheet', 'simple_smartsheet.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0',
 'cattrs>=0.9.0,<0.10.0',
 'marshmallow>=3.0.0b19,<4.0.0',
 'pendulum>=2.0,<3.0',
 'python-decouple>=3.1,<4.0',
 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'simple-smartsheet',
    'version': '0.1.0',
    'description': 'Python library to interact with smartsheets',
    'long_description': None,
    'author': 'Dmitry Figol',
    'author_email': 'git@dmfigol.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)

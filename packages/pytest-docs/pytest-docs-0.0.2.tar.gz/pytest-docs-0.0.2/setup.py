# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_docs', 'pytest_docs.formatters']

package_data = \
{'': ['*']}

install_requires = \
['pytest']

setup_kwargs = {
    'name': 'pytest-docs',
    'version': '0.0.2',
    'description': 'Documentation tool for pytest',
    'long_description': None,
    'author': 'orcarmi',
    'author_email': 'ocarmi@proofpoint.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

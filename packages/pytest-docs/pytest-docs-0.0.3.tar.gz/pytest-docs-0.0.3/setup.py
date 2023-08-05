# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytest_docs', 'pytest_docs.formatters']

package_data = \
{'': ['*']}

install_requires = \
['pytest']

entry_points = \
{'console_scripts': ['license = MIT',
                     'pytest11 = pytest-doc:pytest_docs.plugin']}

setup_kwargs = {
    'name': 'pytest-docs',
    'version': '0.0.3',
    'description': 'Documentation tool for pytest',
    'long_description': '===========\npytest-docs\n===========\n\nDocumentation tool for pytest\n\n.. image:: https://img.shields.io/pypi/v/pytest-docs.svg\n    :target: https://pypi.org/project/pytest-docs\n    :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-docs.svg\n    :target: https://pypi.org/project/pytest-docs\n    :alt: Python versions\n\n.. image:: https://travis-ci.org/liiight/pytest_docs.svg?branch=master\n    :target: https://travis-ci.org/liiight/pytest-docs\n    :alt: See Build Status on Travis CI\n\n----\n\nThis `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_\'s `cookiecutter-pytest-plugin`_ template.\n\n\nFeatures\n--------\n\nCreate documentation of your tests. Current supported formats:\n\n- Markdown\n- reStrcutured text\n\nWhy not sphinx?\n---------------\n\n(More accurately, why not sphinx-autodoc?)\nSphinx is an amazing tool that I use and used in other project. To use its autodoc plugin, it need the documented plugin to be importable by the python interperter. Pytest test collection and invocation uses a completely separate mechanism.\nIf you believe that it somehow possible to use sphinx to create pytest documentation, please do not hesitate to contact me.\n\nRequirements\n------------\n\n- Python 3.4, 3.5, 3.6 or 3.7\n- Pytest >= 3.5.0\n\nInstallation\n------------\n\nYou can install "pytest-docs" via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-docs\n\n\nUsage\n-----\n\nUse ``--docs [PATH]`` to create the documentation.\n\nUse ``--doc-type`` to select the type (currently supports ``md`` and ``rst``)\n\n**Note:** pytest-docs uses the pytest collection mechanism, so your documentation will be generated according the the usual collection commands used to run the tests.\n\nContributing\n------------\nContributions are very welcome. Tests can be run with `tox`_, please ensure\nthe coverage at least stays the same before you submit a pull request.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-docs" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause\n.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt\n.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/liiight/pytest-docs/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.io/en/latest/\n.. _`pip`: https://pypi.org/project/pip/\n.. _`PyPI`: https://pypi.org/project\n',
    'author': 'orcarmi',
    'author_email': 'ocarmi@proofpoint.com',
    'url': 'https://github.com/liiight/pytest_docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)

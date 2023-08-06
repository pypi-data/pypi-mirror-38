# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['euchre', 'euchre.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.0,<7.0', 'minilog>=0.4,<0.5']

setup_kwargs = {
    'name': 'euchre',
    'version': '0.0',
    'description': 'Sample project generated from jacebrowning/template-python.',
    'long_description': 'Unix: [![Unix Build Status](https://img.shields.io/travis/jacebrowning/euchre/develop.svg)](https://travis-ci.org/jacebrowning/euchre) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/euchre/develop.svg)](https://ci.appveyor.com/project/jacebrowning/euchre)<br>Metrics: [![Coverage Status](https://img.shields.io/coveralls/jacebrowning/euchre/develop.svg)](https://coveralls.io/r/jacebrowning/euchre) [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/euchre.svg)](https://scrutinizer-ci.com/g/jacebrowning/euchre/?branch=develop)<br>Usage: [![PyPI Version](https://img.shields.io/pypi/v/Euchre.svg)](https://pypi.org/project/Euchre) [![PyPI License](https://img.shields.io/pypi/l/Euchre.svg)](https://pypi.org/project/Euchre)\n\n# Overview\n\nSample project generated from jacebrowning/template-python.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n# Setup\n\n## Requirements\n\n* Python 3.7+\n\n## Installation\n\nInstall Euchre with pip:\n\n```sh\n$ pip install Euchre\n```\n\nor directly from the source code:\n\n```sh\n$ git clone https://github.com/jacebrowning/euchre.git\n$ cd euchre\n$ python setup.py install\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```sh\n$ python\n>>> import euchre\n>>> euchre.__version__\n```\n',
    'author': 'Euchre',
    'author_email': 'jacebrowning@gmail.com',
    'url': 'https://coverage.space/client/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

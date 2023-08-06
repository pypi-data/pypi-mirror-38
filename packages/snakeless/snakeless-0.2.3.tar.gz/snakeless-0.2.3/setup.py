# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['snakeless', 'snakeless.commands', 'snakeless.mixins', 'snakeless.providers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0',
 'cliff>=2.14,<3.0',
 'fs>=2.1,<3.0',
 'halo>=0.0.21,<0.0.22',
 'schema>=0.6.8,<0.7.0',
 'setuptools>=39']

entry_points = \
{'console_scripts': ['snakeless = snakeless:main'],
 'snakeless.cli': ['check = snakeless.commands:Check',
                   'deploy = snakeless.commands:Deploy']}

setup_kwargs = {
    'name': 'snakeless',
    'version': '0.2.3',
    'description': 'Write true serverless apps with joy',
    'long_description': '# Snakeless [![image](https://img.shields.io/pypi/v/snakeless.svg)](https://python.org/pypi/snakeless) [![image](https://img.shields.io/pypi/l/snakeless.svg)](https://python.org/pypi/snakeless) [![image](https://img.shields.io/pypi/pyversions/snakeless.svg)](https://python.org/pypi/snakeless)\n\n> Write true serverless apps with joy\n\n## Description\n\n**Snakeless** is a tool that tries to simplify deployment of serverless apps on\ndifferent platforms. \n\nIt is easily extensible by plugins. You can write a plugin for additional functionality \nor a wrapper for new service provider!\n\nPlugins for providers:\n- [Google Cloud](https://github.com/Tasyp/snakeless-provider-gcloud)\n- Feel free to write your own!\n\n## Features\n-   Supports multiple serverless providers.\n-   Loads `.env` Automatically. \n-   Configuration is done in one simple `.yaml` file\n-   Wide range of available aspects to configure.\n-   Deploy all functions at once or by one - you choose!\n-   *WIP*: Possible to invoke functions locally \n\n## Usage\n\nWe use [poetry](https://github.com/sdispater/poetry) for dependency management and publishing.\n\n### Installation\n```\n$ pip install snakeless \n```\n\n### Development\n\n```\n$ poetry instal \n```\n\n### Testing\n```\nWIP\n```\n\n## Documentation\nWIP\n\n## Contributions\n\nFeel free to send some [pull request](https://github.com/Tasyp/snakeless/pulls) or [issue](https://github.com/Tasyp/snakeless/issues).\n\n## License\nMIT license\n\n© 2018 [German Ivanov](https://github.com/Tasyp)\n',
    'author': 'German Ivanov',
    'author_email': 'germivanov@gmail.com',
    'url': 'https://github.com/Tasyp/snakeless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

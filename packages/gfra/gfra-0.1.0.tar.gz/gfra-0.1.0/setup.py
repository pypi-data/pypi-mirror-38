# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gfra', 'gfra.decorators']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0']

setup_kwargs = {
    'name': 'gfra',
    'version': '0.1.0',
    'description': 'REST API framework for Google Serverless Functions',
    'long_description': '# gfra [![image](https://img.shields.io/pypi/v/gfra.svg)](https://python.org/pypi/gfra) [![image](https://img.shields.io/pypi/l/gfra.svg)](https://python.org/pypi/gfra) [![image](https://img.shields.io/pypi/pyversions/gfra.svg)](https://python.org/pypi/gfra)\n\n> REST API framework for Google Serverless Functions \n\n## Description\n\n**gfra** stands for **G**oogle **F**unctions **R**EST **A**PI\n\n## Usage\n\nWe use [poetry](https://github.com/sdispater/poetry) for dependency management and publishing.\n\n\n### Installation\n```\n$ poetry add gcloud-functions-rest-api\n```\n\n### Development\n\n```\nWIP\n```\n\n### Production\n```\nWIP\n```\n\n### Testing\n```\nWIP\n```\n\n## Documentation\nWIP\n\n## Contributions\n\nFeel free to send some [pull request](https://github.com/Tasyp/gfra/pulls) or [issue](https://github.com/Tasyp/gfra/issues).\n\n## License\nMIT license\n\n© 2018 [German Ivanov](https://github.com/Tasyp)',
    'author': 'German Ivanov',
    'author_email': 'germivanov@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

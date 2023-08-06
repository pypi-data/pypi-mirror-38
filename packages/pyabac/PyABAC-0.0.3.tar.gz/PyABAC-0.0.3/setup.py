# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['abac', 'abac.db', 'abac.web']

package_data = \
{'': ['*']}

extras_require = \
{'aiohttp': ['aiohttp>=3.4,<4.0'], 'gremlin': ['gremlinpython>=3.3,<4.0']}

setup_kwargs = {
    'name': 'pyabac',
    'version': '0.0.3',
    'description': 'A simple ABAC library for Python.',
    'long_description': 'PyABAC\n======\n\nABAC library for Python 3\n',
    'author': 'Julian DeMille',
    'author_email': 'julian.demille@demilletech.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

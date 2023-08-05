# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['typegql', 'typegql.core']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core-next>=1.0,<2.0', 'uvloop>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'typegql',
    'version': '0.1.1',
    'description': 'A Python GraphQL library that makes use of type hinting and concurrency support with the new async/await syntax.',
    'long_description': None,
    'author': 'Ciprian Tarta',
    'author_email': 'ciprian@cipriantarta.ro',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

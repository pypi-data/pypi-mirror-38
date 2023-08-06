# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['diamond_add_taxonomy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'ete3>=3.1,<4.0', 'six>=1.11,<2.0']

entry_points = \
{'console_scripts': ['diamond_add_taxonomy = '
                     'diamond_add_taxonomy.cli:annotate_diamond']}

setup_kwargs = {
    'name': 'diamond-add-taxonomy',
    'version': '0.1.1',
    'description': 'Tools for working with the NCBI taxonomy database (and DIAMOND output)',
    'long_description': None,
    'author': 'Peter van Heusden',
    'author_email': 'pvh@sanbi.ac.za',
    'url': 'https://github.com/pvanheus/diamond_add_taxonomy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

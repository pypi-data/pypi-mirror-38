# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ncbi_taxid']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'ete3>=3.1,<4.0']

entry_points = \
{'console_scripts': ['diamond_add_taxonomy = ncbi_taxid.cli:annotate_diamond']}

setup_kwargs = {
    'name': 'ncbi-taxid',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Peter van Heusden',
    'author_email': 'pvh@sanbi.ac.za',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

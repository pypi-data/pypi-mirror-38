# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hocus_pocus']

package_data = \
{'': ['*']}

install_requires = \
['invoke']

setup_kwargs = {
    'name': 'hocus-pocus',
    'version': '0.1.0',
    'description': '',
    'long_description': '# hocus pocus\n',
    'author': 'Markus Quade',
    'author_email': 'info@markusqua.de',
    'url': 'https://github.com/Ohjeah/invocations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

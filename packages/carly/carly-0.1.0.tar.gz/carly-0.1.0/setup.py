# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['carly']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=18.9,<19.0']

setup_kwargs = {
    'name': 'carly',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'A tool for putting messages into and collecting responses from Twisted servers using real networking.Chris Withers',
    'author_email': 'chris@withers.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

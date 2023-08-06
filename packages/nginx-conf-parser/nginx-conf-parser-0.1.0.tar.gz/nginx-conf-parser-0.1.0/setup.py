# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nginx_conf_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nginx-conf-parser',
    'version': '0.1.0',
    'description': 'A python library for parsing Nginx Configuration files',
    'long_description': '# Nginx Configuration parser for python\n[![Build Status](https://travis-ci.org/Querdos/nginx-conf-parser.svg?branch=master)](https://travis-ci.org/Querdos/nginx-conf-parser)\n',
    'author': 'Hamza ESSAYEGH',
    'author_email': 'hamza.essayegh@protonmail.com',
    'url': 'https://github.com/Querdos/nginx-conf-parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

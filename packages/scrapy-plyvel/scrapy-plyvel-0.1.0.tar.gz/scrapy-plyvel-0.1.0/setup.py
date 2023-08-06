# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['scrapy_plyvel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scrapy-plyvel',
    'version': '0.1.0',
    'description': 'Scrapy cache storage using plyvel',
    'long_description': None,
    'author': 'Ratson',
    'author_email': 'github@ratson.name',
    'url': 'https://github.com/ratson/scrapy-plyvel',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

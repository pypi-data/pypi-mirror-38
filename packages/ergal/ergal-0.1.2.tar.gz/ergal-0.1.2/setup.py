# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['ergal']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20,<3.0', 'xmltodict>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'ergal',
    'version': '0.1.2',
    'description': 'The Elegant and Readable General API Library',
    'long_description': None,
    'author': 'Elliott Maguire',
    'author_email': 'etgmag@comcast.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

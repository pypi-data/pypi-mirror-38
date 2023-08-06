# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['osumix']

package_data = \
{'': ['*'], 'osumix': ['audio/*']}

install_requires = \
['click>=7.0,<8.0', 'pydub>=0.23.0,<0.24.0', 'slider>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['osumix = osumix.shell:main']}

setup_kwargs = {
    'name': 'osumix',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Justin',
    'author_email': 'jbtcao@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

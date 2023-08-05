# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['click_skeleton']

package_data = \
{'': ['*']}

install_requires = \
['attrdict>=2.0,<3.0',
 'click-completion>=0.5.0,<0.6.0',
 'click-didyoumean>=0.0.3,<0.0.4',
 'click-repl>=0.1.5,<0.2.0',
 'click>=7.0,<8.0',
 'coloredlogs>=10.0,<11.0',
 'pytest-asyncio>=0.9.0,<0.10.0',
 'pytest>=3.8,<4.0',
 'uvloop>=0.11.3,<0.12.0']

entry_points = \
{'console_scripts': ['click-skeleton = click_skeleton.skel:main']}

setup_kwargs = {
    'name': 'click-skeleton',
    'version': '0.1.2',
    'description': 'Click app skeleton',
    'long_description': None,
    'author': 'Adrien Pensart',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)

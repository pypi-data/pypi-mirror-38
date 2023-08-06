# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keydope']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.1,<2.0',
 'inotify_simple>=1.1,<2.0',
 'python-xlib>=0.23.0,<0.24.0',
 'pyyaml>=3.13,<4.0',
 'tabulate>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'keydope',
    'version': '0.1.0a2',
    'description': '',
    'long_description': '# Keydope\n\nKeydope is a flexible keyboard remapping tool written in Python, originally\nforked from [xkeysnail](https://github.com/mooz/xkeysnail).\nIt currently only supports Linux, but support for Windows is planned.\n\nIt can replace tools such as xmodmap, xbindkeys, sxhkd, xchainkeys, and xcape.\n',
    'author': 'infokiller',
    'author_email': None,
    'url': 'https://github.com/infokiller/keydope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['networkparse']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'poetry',
 'pytest-cov',
 'recommonmark',
 'sphinx',
 'sphinx-autobuild',
 'sphinx-rtd-theme']

setup_kwargs = {
    'name': 'networkparse',
    'version': '1.0',
    'description': 'Simple read-only parser for Cisco IOS, NX-OS, HP, and other network device running configs',
    'long_description': 'Installing\n==========\n\n.. code-block::\n\n    pip install --user networkparse\n\nUsing\n=====\nDocs are available on [Read the Docs](https://networkparse.readthedocs.io/en/latest/)\n\n\nLicense\n=======\nThis module was developed by and for [Xylok, LLC](https://www.xylok.io). The code is\nrelease under the MIT license.\n\n\nCredits\n=======\nThis module was inspired by [CiscoConfParse](https://github.com/mpenning/ciscoconfparse).\n',
    'author': 'Ryan Morehart',
    'author_email': 'ryan@xylok.io',
    'url': 'https://gitlab.com/xylok/networkparse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

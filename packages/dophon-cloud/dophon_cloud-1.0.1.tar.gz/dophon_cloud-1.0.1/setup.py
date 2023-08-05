# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon_cloud', 'dophon_cloud.enhance_pkg']

package_data = \
{'': ['*']}

install_requires = \
['dophon', 'dophon_cloud_center']

setup_kwargs = {
    'name': 'dophon-cloud',
    'version': '1.0.1',
    'description': 'dophon cloud(import reg center)',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

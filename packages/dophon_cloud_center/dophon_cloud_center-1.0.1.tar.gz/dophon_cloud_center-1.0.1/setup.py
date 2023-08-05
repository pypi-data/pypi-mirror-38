# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon_cloud_center', 'dophon_cloud_center.kits']

package_data = \
{'': ['*'], 'dophon_cloud_center': ['templates/*']}

install_requires = \
['dophon']

setup_kwargs = {
    'name': 'dophon-cloud-center',
    'version': '1.0.1',
    'description': 'dophon cloud reg center',
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

# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pyartifact', 'pyartifact.types']

package_data = \
{'': ['*']}

install_requires = \
['mypy_extensions>=0.4.1,<0.5.0', 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'pyartifact',
    'version': '0.1.0',
    'description': "Pythonic wrapper around Valve's Artifact API",
    'long_description': None,
    'author': 'David Jetelina',
    'author_email': 'david@djetelina.cz',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

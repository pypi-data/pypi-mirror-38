# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['onedrivefs']

package_data = \
{'': ['*']}

modules = \
['onedrivefs']
install_requires = \
['fs>=2.1,<3.0', 'requests-oauthlib>=1.0,<2.0', 'requests>=2.20,<3.0']

entry_points = \
{'fs.opener': ['onedrive = fs.opener.onedrivefs:OneDriveFSOpener']}

setup_kwargs = {
    'name': 'fs.onedrivefs',
    'version': '0.2.1',
    'description': 'Pyfilesystem2 implementation for OneDrive using Microsoft Graph API',
    'long_description': 'fs.onedrivefs\n=============\n\nImplementation of pyfilesystem2 file system using OneDrive\n\nUsage\n=====\n\n.. code-block:: python\n\n  onedriveFS = OneDriveFS(\n    clientId=<your client id>,\n    clientSecret=<your client secret>,\n    token=<token JSON saved by oauth2lib>,\n    SaveToken=<function which saves a new token string after refresh>)\n\n  # onedriveFS is now a standard pyfilesystem2 file system\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'url': 'https://github.com/rkhwaja/fs.onedrivefs',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

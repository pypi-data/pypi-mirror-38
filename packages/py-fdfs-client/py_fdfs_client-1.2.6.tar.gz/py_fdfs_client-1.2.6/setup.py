#!/usr/bin/env python
import os
from fdfs_client import __version__

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
long_description = f.read()
f.close()

sdict = {
    'name': 'py_fdfs_client',
    'version': __version__,
    'description': 'Python client for Fastdfs ver 4.06',
    'long_description': long_description,
    'author': 'MG',
    'author_email': 'zksfyz@gmail.com',
    'maintainer': 'scott yuan',
    'maintainer_email': 'scottzer8@gmail.com',
    'keywords': ['Fastdfs', 'Distribute File System'],
    'license': 'GPLV3',
    'packages': ['fdfs_client'],
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
    'ext_modules': [Extension('fdfs_client.sendfile',
                              sources=['fdfs_client/sendfilemodule.c'])],
}

setup(**sdict)


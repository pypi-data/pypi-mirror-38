#!/usr/bin/env python

from setuptools import setup

import json_doc

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='json-doc',
    version=json_doc.__version__,
    description="Utility Functions for JSON Document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=json_doc.__author__,
    author_email=json_doc.__email__,
    url="http://github.com/ddfs/json-doc",
    packages=['json_doc', 'tests'],
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    license='Apache Software License',
    keywords=['json', 'document', 'pointer'],
    test_suite='tests',
    tests_require=['unittest2'],
)

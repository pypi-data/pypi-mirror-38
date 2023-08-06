# -*- coding: utf-8 -*-
"""this package is used to deal with logs and category it by automation

:copyright: 
:author: leo
:contact: 
"""
import re
import sys
from os.path import abspath, dirname, join
from setuptools import setup

CURDIR = dirname(abspath(__file__))
REQUIREMENTS = ['scikit-learn >= 0.19.1']
with open(join(CURDIR, 'README.md')) as f:
    DESCRIPTION = f.read()
CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries :: Python Modules
'''.strip().splitlines()

setup(
    name='MachineLearningForTextcategory',
    version='1.0.0',
    description='Machine learning for text category',
    long_description=DESCRIPTION,
    author='leo',
    author_email='liyaowang518@gmail.com',
    url='https://github.com/',
    license='Apache License 2.0',
    keywords='machine learning for dealing with plain text logs',
    platforms='any',
    classifiers=CLASSIFIERS,
    install_requires = REQUIREMENTS,
    package_dir={'':'src'},
    packages=['MachineLearningForTextcategory'],
    scripts=["src/scripts/smart_learn.py"]
)
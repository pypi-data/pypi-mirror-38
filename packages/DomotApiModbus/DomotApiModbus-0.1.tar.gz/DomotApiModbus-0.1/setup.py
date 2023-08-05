#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Home Automation',
]

with open('README.rst') as file_readme:
    readme = file_readme.read()

with open('HISTORY.rst') as file_history:
    history = file_history.read()

with open('requirements.txt') as file_requirements:
    requirements = file_requirements.read().splitlines()

settings.update(
    name='DomotApiModbus',
    version='0.1',
    description='Working with modbus devices in domot-api',
    long_description=readme + '\n\n' + history,
    author='Denis Sacchet',
    license='MIT',
    url='https://github.com/dsacchet/DomotApiModbus',
    classifiers=CLASSIFIERS,
    keywords="modbus vmc boiler dedietrich unelvent ideo",
    py_modules= ['DomotApiModbus','VmcUnelvent'],
    install_requires=requirements,
)


setup(**settings)

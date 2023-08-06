#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

import sys
import os
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

requirements = ['Click>=6.0', 'boto3', 'botocore', 'tenacity']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Martin Schade",
    author_email='git.schade@gmail.com',
    python_requires=">=3.4",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Lex Bot deployment script and function",
    install_requires=requirements,
    scripts=['bin/lex-bot-deploy', 'bin/lex-bot-get-schema'],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lex_bot_deploy',
    name='lex_bot_deploy',
    packages=find_packages(include=['lex_bot_deploy']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Schadix/lex_bot_deploy',
    version='0.1.6',
    zip_safe=False,
)

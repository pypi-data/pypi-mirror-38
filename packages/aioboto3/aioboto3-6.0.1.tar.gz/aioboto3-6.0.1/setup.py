#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # 'aiobotocore~=0.9.4',  # Copied into project :(

    'boto3>=1.9.49,<1.9.50',
    'botocore>=1.12.49,<1.12.50',
    'aiohttp>=3.3.1',  # aiobotocore deps
    'wrapt>=1.10.10',  # aiobotocore deps
]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest',
    'pytest-asyncio',
    'flake8'
]

setup(
    name='aioboto3',
    version='6.0.1',
    description="Async boto3 wrapper",
    long_description=readme + '\n\n' + history,
    author="Terry Cain",
    author_email='terry@terrys-home.co.uk',
    url='https://github.com/terrycain/aioboto3',
    packages=find_packages(include=['aioboto3*']),
    include_package_data=True,
    install_requires=requirements,
    license="Apache 2",
    zip_safe=False,
    keywords='aioboto3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

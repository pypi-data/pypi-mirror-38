#!/usr/bin/env python3.7

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import os.path
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))
version = open(os.path.join(root_dir, 'VERSION')).read()
long_description = open(os.path.join(root_dir, 'README.md')).read()

install_requires = [
    'connexion[aiohttp]>=2.0.2',
    'aioneo4j>=0.0.5',
    'ujson>=1.35',
    'uvloop>=0.11.3'
]

tests_require = [
    'pytest',
    'pytest-cov'
]

setup_requires = [
    'pytest-runner',
    'flake8'
]


class PyTest(TestCommand):

    user_options = [
        ('cov-html=', None, 'Generate html report'),
        ('filter=', None, "Pytest setence to filter (see pytest '-k' option)")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', 'friendsreco', '-xvv']
        self.cov_html = False
        self.filter = False

    def finalize_options(self):
        TestCommand.finalize_options(self)

        if self.cov_html:
            self.pytest_args.extend(['--cov-report', 'html'])
        else:
            self.pytest_args.extend(['--cov-report', 'term-missing'])

        if self.filter:
            self.pytest_args.extend(['-k', self.filter])

        self.pytest_args.extend(['tests'])

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='friendsreco',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    description='A simple HTTP friends recommendations service.',
    long_description=long_description,
    author='Diogo Dutra',
    author_email='diogodutradamata@gmail.com',
    url='https://github.com/dutradda/friendsreco',
    keywords='recomendations service graph neo4j',
    license='MIT',
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP'
    ],
    entry_points={
        'console_scripts': [
            'friendsreco = friendsreco.run:main'
        ]
    }
)

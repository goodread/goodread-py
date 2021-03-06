# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
PACKAGE = 'goodread'
INSTALL_REQUIRES = [
    'six>=1.9,<2.0',
    'click>=6.0,<7.0',
    'emoji>=0.4,<1.0',
    'pyyaml>=3.1,<4.0',
    'requests>=2.8,<3.0',
]
TESTS_REQUIRE = [
    'pylama',
    'tox',
]
README = read('README.md')
VERSION = read(PACKAGE, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name=PACKAGE,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'develop': TESTS_REQUIRE},
    entry_points={
        'console_scripts': [
            'goodread-py = goodread.cli:cli',
        ]
    },
    zip_safe=False,
    long_description=README,
    description='Doctest for markdown with comment-based assertions. Python/JavaScript/Ruby/PHP test runners and hackmd.io integration.',
    author='Evgeny Karev',
    author_email='eskarev@gmail.com',
    url='https://github.com/goodread/goodread-py',
    license='MIT',
    keywords=[
        'goodread',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

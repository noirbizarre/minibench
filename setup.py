#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

import codecs
import re

from setuptools import setup, find_packages

RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')

PYPI_RST_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+',  '::'),
    # Remove all badges
    (r'\.\. image:: .*', ''),
    (r'    :target: .*', ''),
    (r'    :alt: .*', ''),
)


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - all badges
    '''
    content = codecs.open(filename, encoding='utf-8').read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

# Import metadatas
exec(compile(open('minibench/__about__.py').read(),
             'minibench/__about__.py', 'exec'))

tests_require = ['nose', 'rednose', 'markdown', 'docutils']
install_requires = ['click', 'six']
dev_requires = ['invoke', 'tox', 'flake8', 'sphinx', 'sphinx_rtd_theme', 'bumpr']

setup(
    name='minibench',
    version=__version__,
    description=__description__,
    long_description=long_description,
    url=__url__,
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev': dev_requires,
    },
    entry_points={
        'console_scripts': [
            'bench = minibench.cli:cli',
        ]
    },
    license='MIT',
    zip_safe=False,
    keywords='benchmark test development reporting performance',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)

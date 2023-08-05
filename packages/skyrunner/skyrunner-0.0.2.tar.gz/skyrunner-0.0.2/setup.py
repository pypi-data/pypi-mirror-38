#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

def _requires_from_file(filename):
    return open(filename).read().splitlines()

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here,
                                              'skyrunner',
                                              '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.2')

setup(
    name="skyrunner",
    version=version,
    url='https://github.com/globallines-developers/skyrunner',
    author='Yusuke Kobayashi',
    author_email='yusuke.kobayashi@mileshare.jp',
    maintainer='Yusuke Kobayashi',
    maintainer_email='yusuke.kobayashi@mileshare.jp',
    description='Skyrunner scrapes with json definition',
    long_description=readme,
    packages=find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ]
)

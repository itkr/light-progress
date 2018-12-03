# -*- encoding:utf-8 -*-

import os
from io import open

from setuptools import setup

from light_progress import __version__

document_file = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(document_file, 'r', encoding='utf-8_sig') as f:
    long_description = f.read()


setup(
    name='light-progress',
    version=__version__,
    packages=['light_progress'],
    description='Light progress reporting tool for Python',
    long_description=long_description,
    url='https://github.com/itkr/light-progress',
    license='MIT',
    author='itkr',
    author_email='itkrst@gmail.com',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)

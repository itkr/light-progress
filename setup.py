# -*- encoding:utf-8 -*-

import os
from setuptools import setup

from light_progress import __version__

# def get_requirements():
#     with open('requirements.txt') as f:
#         requirements = f.read().split('\n')
#     return requirements

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
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
    # install_requires=get_requirements(),
    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities'
    ]
)

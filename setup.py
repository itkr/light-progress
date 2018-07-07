# -*- encoding:utf-8 -*-
from setuptools import setup


def get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().split('\n')
    return requirements


setup(
    name="progress_bar",
    version="0.0.1",
    packages=['progress_bar'],
    description='Progress bar',
    long_description='Light progress reporting tool for Python',
    url='https://github.com/itkr/progress_bar',
    license='MIT',

    author='itkr',
    author_email='itkrst@gmail.com',

    install_requires=get_requirements(),

    classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Utilities'
    ]
)

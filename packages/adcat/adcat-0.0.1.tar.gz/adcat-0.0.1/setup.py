# -*- coding: utf-8 -*-
"""setup.py."""

from setuptools import setup, find_packages


VERSION = '0.0.1'

LONG_DESCRIPTION = 'adcat is Algorithm and DataStructure toolbox write in python'

setup(
    name='adcat',
    version=VERSION,
    description='adcat is Algorithm and DataStructure toolbox write in python',
    long_description=LONG_DESCRIPTION,
    author='silence',
    author_email='istommao@gmail.com',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/istommao/adcat',
    keywords='adcat is Algorithm and DataStructure toolbox write in python'
)

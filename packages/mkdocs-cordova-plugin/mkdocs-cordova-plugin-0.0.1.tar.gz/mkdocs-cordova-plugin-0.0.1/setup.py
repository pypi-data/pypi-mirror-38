#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="mkdocs-cordova-plugin",
    version='0.0.1',
    url='https://gitlab.com/lramage94/mkdocs-cordova-plugin',
    license='MIT',
    description='Deploy documentation to any mobile device via Apache Cordova',
    long_description=read('README.md'),
    keywords='mkdocs python markdown cordova apache mobile',
    author='Lucas Ramage',
    author_email='ramage.lucas@protonmail.com',
    include_package_data=True,
    install_requires=[
        'mkdocs>=0.17'
    ],
    packages=find_packages(exclude=['*.tests']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    entry_points={
        'mkdocs.plugins': [
            'cordova = cordova:CordovaPlugin',
        ],
    },
    zip_safe=False,
)

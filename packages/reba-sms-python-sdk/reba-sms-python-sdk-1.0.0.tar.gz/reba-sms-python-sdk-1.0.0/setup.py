# -*- coding:utf-8 -*-
# filename:setup

__author__ = 'reba'
from setuptools import setup, find_packages

setup(
    name='reba-sms-python-sdk',
    version='1.0.0',
    keywords=('reba', 'sms', 'sdk'),
    description='reba python sdk',
    license='MIT',
    install_requires=['requests>=2.9.1'],
    author='shomop',
    author_email='lanran@shomop.com',
    packages=find_packages(),
    platforms='any',
)

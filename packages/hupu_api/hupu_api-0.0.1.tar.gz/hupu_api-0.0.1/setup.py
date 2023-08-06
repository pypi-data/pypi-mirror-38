#!/usr/bin/env python
# coding: utf-8
# Created by BBruceyuan on 18-11-23.


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import hupu_api

setup(
    name='hupu_api',  # pip install 的时候的名字
    version=hupu_api.__version__,
    author=hupu_api.__author__,
    author_email='bruceyuan123@gmail.com',
    license='MIT',
    url='https://github.com/hey-bruce/hupu-api',
    keywords=['hupu', 'hoop', 'http', 'api', 'JSON'],
    description='尝试解析出虎扑(hupu,hoop)的API接口，并提供优雅的使用方式，方便二次开发',
    packages='',
    install_requires=[
        'requests >=  2.20.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

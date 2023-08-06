#!/usr/bin/env python
#-*- coding:utf-8 -*-

############################################# # File Name: setup.py # Author: xingming # Mail: huoxingming@gmail.com # Created Time: 2015-12-11 01:25:34 AM #############################################


from setuptools import setup, find_packages

setup(
    name = "kkapi",
    version = "1.2",
    description = "半垢API",
    long_description = "半垢專屬使用API",
    license = "MIT 育柔",

    author = "育柔",
    maintainer = "育柔",

    packages = find_packages(),
    include_package_data = True,
    install_requires = []
)
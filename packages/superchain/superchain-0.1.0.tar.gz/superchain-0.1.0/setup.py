#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time: 2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="superchain",
    version="0.1.0",
    keywords=("pip", "superchain"),
    description="A complex chained relational data structure",
    long_description="A complex chained relational data structure",
    license="MIT Licence",

    url='https://github.com/yunlongying/SuperChain.git',
    author='yingyunlong',
    author_email='fengyuan1210@163.com',

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)

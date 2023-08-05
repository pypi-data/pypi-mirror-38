#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Peng Xi
# Mail: px11@my.fsu.edu
# Created Time:  Dec. 16th, 2017
#############################################

from setuptools import setup, find_packages  

setup(
    name = "hirschman",      #这里是pip项目发布的名称
    version = "1.0.3",  #版本号，数值大的会优先被pip
    keywords = ("pip", "hirschman","computations"),
    description = "hirschman related computations",
    long_description = "To calculated hirschman related computations",
    license = "MIT Licence",

    url = "https://github.com/aes3219563/Hirschman-Transform-Lib",     
    author = "Peng Xi",
    author_email = "px11@my.fsu.edu",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]          
)


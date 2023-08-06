#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: raymonYuan
# Mail:1131510575@qq.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "lianjia",
    version = "0.0.1",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
    description = "get lianjia houses data",
    long_description = "time and path tool",
    license = "MIT Licence",

    url = "https://github.com/raymonYuan/raymonYuan.github.io",
    author = "raymonYuan",
    author_email = "1131510575@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pyquery","pymongo","pyecharts"]
)

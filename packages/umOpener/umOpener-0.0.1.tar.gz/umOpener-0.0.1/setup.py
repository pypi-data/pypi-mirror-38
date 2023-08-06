#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: neo
# Mail: james_neo@163.com
# Created Time:  2018-11-18
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "umOpener",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "umOpener","opener"),
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
    license = "MIT Licence",

    url = "https://github.com/XiaoXiaowukong/opener",     #项目相关文件地址，一般是github
    author = "neo",
    author_email = "james_neo@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []          #这个项目需要的第三方库
)

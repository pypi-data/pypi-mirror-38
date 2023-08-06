#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: neo
# Mail: james_neo@163.com
# Created Time:  2018-11-18
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="umOpener",  # 这里是pip项目发布的名称
    version="0.0.8",  # 版本号，数值大的会优先被pip
    keywords=("pip", "umOpener", "opener"),
    description="netcdf4/GeoTiff/ENVI/grib(only read) read and wirte",
    long_description="""
umOpener
=====

netcdf4/GeoTiff/ENVI/ read and wirte
------------

1. nc<--->nc
2. tif<--->tif
3. img<--->img
4. nc<--->tif
5. nc<--->img
6. tif<--->nc
7. tif<--->img
8. img<--->nc
9. img<--->tif
10.read grib2
""",
    license="MIT Licence",

    url="https://github.com/XiaoXiaowukong/opener",  # 项目相关文件地址，一般是github
    author="neo",
    author_email="james_neo@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['netCDF4', 'numpy']  # 这个项目需要的第三方库
)

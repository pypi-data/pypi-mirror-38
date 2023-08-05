#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "yangyaya",      #这里是pip项目发布的名称
    version = "1.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "yangyuya-test","featureextraction"),
    description = "An feature extraction algorithm",
    long_description = "An feature extraction algorithm, improve the FastICA",
	url='https://github.com/zhanghang-z',
    author = "LiangjunFeng",
    author_email = "zhumavip@163.com",
    packages =  ['test'],
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]          #这个项目需要的第三方库
)

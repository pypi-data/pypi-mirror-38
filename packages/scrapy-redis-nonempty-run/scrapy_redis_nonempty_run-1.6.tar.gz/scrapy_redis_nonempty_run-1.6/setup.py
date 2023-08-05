#!/usr/bin/env python
# coding=utf-8

#############################################
# File Name: setup.py
# Author: yangyuya
# Mail: 1019177406@qq.com
# Created Time:  2018-11-5 13:58:00
#############################################

from setuptools import setup, find_packages            

setup(
    name="scrapy_redis_nonempty_run",
    version="1.6",
    keywords=("pip", "scrapy-redis-nonempty_run"),
    description="deal with scrapy-redis's the problem of empty run",
    long_description="",
    license="MIT Licence",
    url="https://github.com/xiaoyangjie/scrapy-redis-noemptyrun",
    author="yangyuya",
    author_email="1019177406@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["Scrapy>=1.0", "redis>=2.10",
                      "six>=1.5.2"]
)
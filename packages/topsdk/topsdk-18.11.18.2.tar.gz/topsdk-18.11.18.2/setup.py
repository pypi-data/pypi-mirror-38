#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='topsdk',
    version='18.11.18.2',  # 按日期
    author='top',
    author_email='xuteng.xt@alibaba-inc.com',
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    long_description_content_type="text/markdown",
    long_description='淘宝联盟topsdk,进行导购推广,有了它，不需要去写爬虫抓取联盟商品信息'
)

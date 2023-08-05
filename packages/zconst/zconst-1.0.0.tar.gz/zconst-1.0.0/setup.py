#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zconst',  # 上传到网站后将显示在网页上的模块名字
    version='1.0.0',
    py_modules=[],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='常量常用包,包括三种常量实现方式, 1:基类继承, 2:装饰器, 3:元类metaclass',
    long_description=open('README.md', 'r', encoding='utf8').read(),  # 项目介绍
    long_description_content_type='text/markdown',
    url='https://pypi.org/',
    license='GNU GENERAL PUBLIC LICENSE',
    platforms=['all'],
    scripts=[],  # 额外的文件
    install_requires=[],  # 依赖库
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)

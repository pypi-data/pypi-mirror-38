#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='zinifile',
    version='1.0.4',
    py_modules=['zinifile'],
    author='zlyuan',
    author_email='1277260932@qq.com',
    packages=find_packages(),
    description='操作更方便的配置文件读取模块',
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

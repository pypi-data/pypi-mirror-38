#!/usr/bin/env python

# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(

    name="my_api",
    version="0.1.2",
    url="https://github.com/li010101/myapi.git",
    author="li010101",
    author_email="liyaohui54@gmail.com",
    long_description=open('README.rst','rb').read(),
    license = "MIT Licence",
    packages=find_packages(),
    install_requires = ["requests"]
)
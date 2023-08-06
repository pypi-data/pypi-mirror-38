# -*- coding: utf-8 -*-
# @Time         : 2018/11/26 下午7:04
# @Author       : luoyeqi
# @Email        : luoyeqi@duoshoubang.cn
# @FileName     : setup.py
# @Description  :

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dirtreegen',
    version='0.0.2',
    author='pythonqi',
    author_email='pythonqi@outlook.com',
    description='Generate directory tree',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    license='MIT',
    install_requires = ['anytree==2.4.3', 'six==1.11.0'],
    url='https://github.com/pythonqi/dirtreegen',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        dirtreegen=dirtreegen:treegen
    """,
)
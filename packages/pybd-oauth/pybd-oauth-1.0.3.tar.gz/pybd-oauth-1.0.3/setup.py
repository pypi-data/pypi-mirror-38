# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.3'


setup(
    name='pybd-oauth',
    version=version,
    keywords='Baidu XiongZhang Oauth Oauth2',
    description='Baidu XiongZhang Oauth Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pybd-oauth',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pybd_oauth'],
    py_modules=[],
    install_requires=['pybd_base>=1.0.2', 'shortuuid'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

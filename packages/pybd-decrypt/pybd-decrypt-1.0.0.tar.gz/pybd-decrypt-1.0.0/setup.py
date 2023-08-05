# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.0'


setup(
    name='pybd-decrypt',
    version=version,
    keywords='Baidu Decrypt',
    description='Baidu Decrypt Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pybd-decrypt',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pybd_decrypt'],
    py_modules=[],
    install_requires=['pycrypto', 'pywe_utils'],

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

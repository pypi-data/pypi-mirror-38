from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="tf-common",
    version="1.0.0",
    author="Terry",
    author_email="335208143@qq.com",
    description="A common liberary of tensorflow",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/terryyrliang",
    packages=['tfcommon'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'tensorflow>=1.7.0',
        'numpy>=1.14.3',
    ],
    zip_safe=True,
)

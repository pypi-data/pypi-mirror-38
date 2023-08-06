#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="bye-bye-shopify",
    version="0.0.1",
    url="https://github.com/jbasko/bye-bye-shopify",
    license="MIT",
    author="Jazeps Basko",
    author_email="jazeps.basko@gmail.com",
    maintainer="Jazeps Basko",
    maintainer_email="jazeps.basko@gmail.com",
    description="Extract product catalogue (including images) from your Shopify store to JSON files",
    keywords="shopify extract export products images json",
    long_description=read("README.rst"),
    packages=["bye_bye_shopify"],
    python_requires=">=3.6.0",
    install_requires=[
        "aarghparse>=0.2.0",
        "requests",
        "strictus-dictus>=0.0.12",
        "wr-profiles",
    ],
    entry_points={
        "console_scripts": [
            "bye-bye-shopify = bye_bye_shopify.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
    ],
)

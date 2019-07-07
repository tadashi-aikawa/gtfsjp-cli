#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        return f.read()


requirements = ["sqlalchemy", "halo", "owcli>=0.6.1"]

setup(
    name="gtfsjp-cli",
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open("gtfsjpcli/main.py").read(),
    ).group(1),
    description="TODO: description",
    long_description=load_readme(),
    long_description_content_type="text/markdown",
    author="__yourname",
    author_email="__youraddress",
    maintainer="__yourname",
    maintainer_email="__youraddress",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements,
    entry_points={"console_scripts": ["gtfsjp = gtfsjpcli.main:main"]},
    classifiers=["Programming Language :: Python", "Programming Language :: Python :: 3"],
)

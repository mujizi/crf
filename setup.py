#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except Exception:
    README = ''
VERSION = "1.0.1"

requirments = ["modelhub", "sklearn_crfsuite", "joblib", "requests", "intervaltree", "pyyaml",
               "spacy==1.10.1", "figure_extractor_en==0.0.8"]

setup(
    name='figure_en',
    version=VERSION,
    description='figure_en',
    url="http://git.patsnap.com/research/figure_en",
    long_description=README,
    author='benqi.wang',
    author_email='wangbenqi@patsnap.com',
    packages=find_packages(exclude=('notebooks', 'tests')),
    install_requires=requirments,
    extras_require={
    },
)

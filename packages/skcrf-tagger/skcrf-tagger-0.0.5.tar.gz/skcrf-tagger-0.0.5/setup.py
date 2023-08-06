#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: InfinityFuture
# Mail: infinityfuture@foxmail.com
# Created Time: 2018-09-06 10:00:00
#############################################

import os
from setuptools import setup, find_packages

version = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    'version.txt'
)

setup(
    name = 'skcrf-tagger',
    version = open(version, 'r').read().strip(),
    keywords = ('pip', 'scikit-learn', 'sklearn-crfsuite', 'CRF', 'NER', 'tagger'),
    description = 'NLP tool',
    long_description = 'NLP tool, NER, POS',
    license = 'MIT Licence',

    url = 'https://github.com/infinity-future/skcrf-tagger',
    author = 'infinityfuture',
    author_email = 'infinityfuture@foxmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['sklearn-crfsuite', 'tqdm', 'scikit-learn', 'numpy', 'scipy']
)

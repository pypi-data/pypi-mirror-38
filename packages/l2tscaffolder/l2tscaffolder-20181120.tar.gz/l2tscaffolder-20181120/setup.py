#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is the setup file for the project."""
import os
import glob

from setuptools import find_packages
from setuptools import setup

import l2tscaffolder

setup(
    name='l2tscaffolder',
    version=l2tscaffolder.__version__,
    description=(
        'Scaffolder project for l2t, helping to bootstrap l2t development.'),
    license='Apache License, Version 2.0',
    url='https://github.com/log2timeline/PlasoScaffolder',
    maintainer='Log2Timeline maintainers',
    maintainer_email='log2timeline-maintainers@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'l2tscaffolder.templates': ['*.jinja2'],'':['.style.yapf']},
    install_requires=['Click>=6.7',
                      'setuptools>=35.0.2',
                      'jinja2>=2.9.6',
                      'colorama>=0.3.7',
                      'yapf==0.22',
                      'timeout-decorator>=0.4.0',
                      'pexpect>=4.2.1'],
    scripts=glob.glob(os.path.join('tools', '[a-z]*.py')),
    keywords="plaso l2t scaffolder log2timeline turbinia timesketch",
)

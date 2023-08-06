#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
imread evaluation
"""
from setuptools import setup

import io
import setuptools

with io.open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(name='imreadeval',
    version='0.1.8',
    description='An evaluation to python imread functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    url='http://github.com/quxiaofeng/imreadeval',
    author='QU Xiaofeng',
    author_email='xiaofeng.qu@aqara.com',
    install_requires=[
          'Pillow',
          'opencv-python',
          'matplotlib',
          'imageio',
          'scipy',
          'scikit-image',
          'pytest'
      ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    license='MIT license, Copyright (c) 2018 QU Xiaofeng',
    packages=setuptools.find_packages(exclude=['tests', '.gitignore', 'packaging.sh']),
    include_package_data=True,
    zip_safe=False
    )


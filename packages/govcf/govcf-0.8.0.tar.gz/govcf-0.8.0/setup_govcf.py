#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('src/govcf/README.md') as readme_file:
    readme = readme_file.read()

history = ""

tests_require = [
    "addict >= 2.1.3",
    "pytest-flake8 >= 1.0.1",
    "pytest >= 3.6.0",
    "pytest-cov >= 2.5.1",
    "pytest-mccabe >= 0.1",
]

setup(
    name="govcf",
    version='0.8.0',
    author="Ian Maurer",
    author_email='ian@genomoncology.com',

    packages=[
        "govcf",
        "govcf.calculate_vaf",
    ],
    package_dir={
        '': 'src'
    },

    package_data={
    },

    include_package_data=True,

    install_requires=[
        "pysam >= 0.14.1",
        "intervaltree",
        "related",
    ],

    tests_require=tests_require,

    setup_requires=[
        'pytest-runner',
    ],

    license="Proprietary",

    keywords='Bioinformatics HGVS VCF Clinical Trials Genomics',
    description="govcf",
    long_description=readme,
    long_description_content_type='text/markdown',

    entry_points={
    },

    classifiers=[
        'License :: Other/Proprietary License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
)

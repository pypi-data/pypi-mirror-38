#!/usr/bin/env python
from __future__ import print_function  
from setuptools import setup

setup(
    name = "sam2pairview",
    version = "1.0.7",
    packages = ['sam2pairview'],
    package_data = {"sam2pairview":["README.md"]},
    install_requires = [
            "pysam",
    ],
    author="Yong Deng",
    author_email = "yodeng@tju.edu.com",
    description = "sam2pairview takes a SAM|BAM file and uses the CIGAR and MD tag to reconstruct the pairwise alignment of each read.",
    license="MIT",
    entry_points = {
        'console_scripts': [  
            'sam2pairview= sam2pairview.sam2pairview:main'
        ]
    }

)

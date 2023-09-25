"""Python package setup."""
import os
from json import load

from setuptools import find_packages, setup

with open('README.md') as in_file:
    long_description = in_file.read()

setup(
    name='tpir',
    version='0.1',
    description="Communications with ATMI TPIR.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/numat/tpir/',
    author="Patrick Fuller",
    author_email='pat@numat-tech.com',
    packages=find_packages(),
    install_requires=[
        'pyserial',
        'async-timeout',
    ],
    entry_points={
        'console_scripts': [
            'tpir = tpir.server:main',
        ]
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Chemistry"
    ]
)

import os
import sys

if sys.version_info < (3,3):
    sys.exit('Sorry, Python < 3.3 is not supported')

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='jupyter-openbis-extension',
    version= '0.0.1',
    author='Swen Vermeul |  ID SIS | ETH Zürich',
    author_email='swen@ethz.ch',
    description='Extension for Jupyter notebooks to connect to openBIS and download/upload datasets, inluding the notebook itself',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://sissource.ethz.ch/sispub/jupyter-openbis-integration',
    packages=find_packages(),
    license='Apache Software License Version 2.0',
    install_requires=[
        'jupyter',
        'pybis',
    ],
    python_requires=">=3.3",
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)

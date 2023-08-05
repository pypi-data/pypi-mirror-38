from setuptools import setup, find_packages
from os import path
from io import open

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="qubiter",
    version="0.0.0",
    author="Artiste-qb",
	keywords = ('quantum compiler'),
    author_email="Robert.Tucci@artiste-qb.net",
    description="Python tools for reading, writing, compiling, simulating quantum computer circuits.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artiste-qb-net/qubiter",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	install_requires=[
        'numpy',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
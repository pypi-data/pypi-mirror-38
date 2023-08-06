#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="martyr",
    author="Maxime Istasse",
    author_email="istassem@gmail.com",
    license='MIT',
    version="0.0.1",
    python_requires='>=3.4',
    packages=find_packages(include=["martyr"]),
    install_requires=["psutil"],
)
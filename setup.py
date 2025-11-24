#!/usr/bin/env python3
"""
Setup script for the Lexical and Semantic Analyzer
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lexical-semantic-analyzer",
    version="1.0.0",
    author="Santiago Patricio Irigoyen Vazquez",
    author_email="santiago@example.com",
    description="A lexical and semantic analyzer for C-like language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IrigoyenCodes/ABET-SO1-M1-Computer-Theory",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Compilers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "lex-analyzer=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

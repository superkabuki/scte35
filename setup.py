#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open("fu/version.py","r", encoding="utf-8") as latest:
    version = latest.read().split('"')[1]

setuptools.setup(
    name="fu",
    version=version,
    author="Adrian of Doom",
    author_email="spam@iodisco.com",
    description="fu is a SCTE-35 Decoder and Encoder for MPEGTS, HLS and Everything else.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/superkabuki/scte35",
    install_requires=[
        'iframes >= 0.0.7',
        'm3ufu >= 0.0.89',
        'new_reader >= 0.1.11',
        'sideways >= 0.0.23',
        "pyaes",
    ],

    scripts=['bin/fu'],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: OpenBSD",
        "Operating System :: Linux",
        "Operating System :: Plan9",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6",
)

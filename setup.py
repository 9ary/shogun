#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name = "Shogun",
    version = "0.1.2",
    packages = find_packages(),
    package_data = { "": ["templates/*"] },
    install_requires = list(open("requirements.txt")),
    author = """Dan "Streetwalrus" Elkouby""",
    author_email = "streetwalrus@codewalr.us",
    description = "A dead simple build system based on Ninja",
    keywords = "ninja build c c++",
    license = "MIT",
    url = "https://github.com/Streetwalrus/shogun"
)

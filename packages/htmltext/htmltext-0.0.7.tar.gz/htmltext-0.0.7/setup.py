# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htmltext",
    version="0.0.7",
    author="Robin Zhang",
    author_email="whycoding@outlook.com",
    description="Get title and main body text from an article in a web page\r\nBug Patched",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RobinZhangWhyCoding/htmltext",
    packages=setuptools.find_packages(),
    install_requires = ['beautifulsoup4',"lxml"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
)

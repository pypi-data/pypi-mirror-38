#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(
    name = 'OnionSVG',
    version = 'v0.1',
    description = 'Peel your SVG files with Python',
    author = 'ybnd',
    author_email = 'ybnd@tuta.io',
    url = 'https://github.com/ybnd/OnionSVG',
    download_url = 'https://github.com/ybnd/OnionSVG/archive/v0.1.tar.gz',
    install_requires = ['lxml', 'cairosvg'],
)
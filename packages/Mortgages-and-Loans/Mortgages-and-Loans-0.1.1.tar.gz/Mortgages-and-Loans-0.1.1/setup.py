# /usr/bin/env python

# This file is part of Mortgages-and-Loans.

# Types-and-Variables is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Mortgages-and-Loans is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Mortgages-and-Loans.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="Mortgages-and-Loans",
    version="0.1.1",
    install_requires=["re", "string"],
    description="Simple Python Scripts for Complex Mortgages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="harens",
    author_email="harensdeveloper@gmail.com",
    url="https://harens.github.io",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="homework, mortgages, loans",
)

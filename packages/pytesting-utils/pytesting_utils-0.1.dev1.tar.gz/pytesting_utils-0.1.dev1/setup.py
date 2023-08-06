#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of PyTesting utils.
#
# PyTesting utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyTesting utils is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyTesting utils.  If not, see <https://www.gnu.org/licenses/>.
import os
import re
from setuptools import setup, find_packages

# Determine version in a more robust way than importing test-runner,
# cf http://gehrecke.de/2014/02/distributing-a-python-command-line-application/
with open("pytesting_utils/__init__.py") as f:
    version = re.search('^__version__[ ]*=[ ]*"(.*)"', f.read(), re.M).group(1)

# Get the long description from the read-me file
readme = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
try:
    import pypandoc

    long_description = pypandoc.convert_file(
        readme, "rst", format="markdown_github-hard_line_breaks"
    )
except (IOError, ImportError):
    with open(readme, "rb") as f:
        long_description = f.read().decode("utf-8")

with open("requirements.txt") as f:
    required_packages = []
    for line in f.readlines():
        required_packages.append(line)

with open("dev-requirements.txt") as f:
    dev_required_packages = required_packages
    for line in f.readlines():
        if "requirements.txt" not in line:
            dev_required_packages.append(line)

setup(
    name="pytesting_utils",
    version=version,
    author="Stephan Lukasczyk",
    author_email="python-test-runner@googlegroups.com",
    description="Utilites for the PyTesting project",
    long_description=long_description,
    url="https://github.com/pytesting/utils",
    license="GNU General Public License (GPLv3)",
    keywords="test runner unittest nose pytest utils",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later ("
        "GPLv3+)",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: Utilities",
    ],
    platforms=["Linux", "macOS", "POSIX"],
    packages=find_packages(),
    install_requires=required_packages,
    setup_requires=dev_required_packages,
    test_suite="py.test",
    zip_safe=True,
)

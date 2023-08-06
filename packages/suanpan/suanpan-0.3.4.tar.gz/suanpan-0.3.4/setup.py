#!/usr/bin/env python

"""
suanpan
"""
import os

from setuptools import find_packages, setup

REQUIREMENTS_FOLDER = "requirements"
REQUIREMENTS = "base"
EXTRA_REQUIREMENTS = ["service", "docker"]
README = "README.md"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def read_requirements(path, folder=REQUIREMENTS_FOLDER):
    return read_file(os.path.join(folder, "{}.txt".format(path))).splitlines()


setup(
    name="suanpan",
    version="0.3.4",
    packages=find_packages(),
    license="See License",
    author="majik",
    author_email="me@yamajik.com",
    description=read_file(README),
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=read_requirements(REQUIREMENTS),
    extras_require={i: read_requirements(i) for i in EXTRA_REQUIREMENTS},
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

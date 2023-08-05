# coding: utf-8

"""
    blu-lib-trend

    This is a package for get trend

    OpenAPI spec version: 0.2.8
    Contact: master@bluehack.net
"""

from setuptools import setup, find_packages

NAME = "blu-lib-trend"
VERSION = "0.2.8"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["selenium",
            "chromedriver_binary"]

setup(
    name=NAME,
    version=VERSION,
    description="get trend package",
    author_email="master@bluehack.net",
    url="",
    keywords=["blu", "blu-lib-trend"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)

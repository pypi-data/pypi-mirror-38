#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='limits-exporter',
    version='0.0.2',
    include_package_data = True,
    packages = find_packages(),
    author = "Felix Ehrenpfort",
    author_email = "felix.ehrenpfort@codecentric.cloud",
    description = "prometheus exporter for openstack compute limits in projects",
    url = "https://github.com/cloudcentric/limits_exporter",
    package_data = {},
    scripts=['bin/limits_exporter'],
    install_requires=[],
    zip_safe=False
)

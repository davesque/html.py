from setuptools import setup, find_packages

import parse_html


setup(
    name='parse_html',
    version=parse_html.version,
    packages=find_packages(),
    test_suite='parse_html.tests',
)

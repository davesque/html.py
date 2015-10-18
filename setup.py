from setuptools import setup, find_packages

import parse_html


setup(
    name='parse_html',
    version=parse_html.version,
    packages=find_packages(),
    test_suite='parse_html.tests',
    install_requires=[
        'parsing==0.1',
    ],
    dependency_links=[
        'https://github.com/davesque/parsing.py/tarball/master#egg=parsing-0.1',
    ],
)

#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-dynamic-subdomains-ai',
    description="Dynamic and static subdomain support for Django.",
    version='0.2.2',
    url='https://github.com/andersinno/django-dynamic-subdomains',

    author='Anders',
    author_email='admin@anders.fi',
    license='BSD',

    packages=find_packages(),
    package_data={
        'dynamic_subdomains': [
            'templates/*/*.html',
        ],
    },
)

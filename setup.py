# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-xfeed',
    version='0.0.1',
    author=u'Ruud Schroën',
    author_email='schroenruud@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/rschroen/django-xfeed',
    license='MIT licence, see LICENCE.txt',
    description='A reusable application for Django, that aims to be a single '
                'aggregator for various media types (e.g. RSS, Twitter, Facebook).',
    long_description=open('README.md').read(),
    zip_safe=False,
)

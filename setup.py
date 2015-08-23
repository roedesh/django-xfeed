# -*- coding: utf-8 -*-
import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-xfeed',
    version='0.0.1',
    packages=['xfeed'],
    include_package_data=True,
    license='BSD License',
    description='A reusable application for Django, that aims to be a single '
                'aggregator for various media types (e.g. RSS, Twitter, Facebook).',
    long_description=README,
    url='https://github.com/rschroen/django-xfeed',
    author='Ruud Schroën',
    author_email='schroenruud@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
#!/usr/bin/env python

import os

from setuptools import setup, find_packages

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURRENT_PATH, 'requirements.txt')) as f:
    required = f.read().splitlines()


setup(
    name='django-acmin',
    version="0.1.8",
    author='Hike Li',
    author_email='hikelee@gmail.com',
    url='https://github.com/hikelee/django-acmin',
    description='Admin and API template for start a django web',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django :: 2.1',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    license='BSD',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    zip_safe=False,
)

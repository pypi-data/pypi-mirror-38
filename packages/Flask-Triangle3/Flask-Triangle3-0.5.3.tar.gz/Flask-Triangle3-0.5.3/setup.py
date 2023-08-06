#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='Flask-Triangle3',
    version='0.5.3',
    author='Morgan Delahaye-Prat',
    author_email='mdp@m-del.fr',
    description=('Integration of AngularJS and Flask.'),
    long_description=open('README.rst').read(),
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=['six', 'flask', 'jsonschema'],
    tests_require=['beautifulsoup4'],
    url='https://github.com/Lightslayer/flask-triangle',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

from setuptools import setup, find_packages


__author__ = __import__('easyauth').__version__


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


setup(
    name='easyauth',
    version=__import__('easyauth').__version__,
    author=__import__('easyauth').__author__,
    author_email='qingfeng0820@sina.com',
    maintainer=__import__('easyauth').__author__,
    maintainer_email='qingfeng0820@sina.com',
    url='https://github.com/qingfeng0820/easyauth',
    license=__import__('easyauth').__license__,
    # packages=find_packages(),
    packages=find_packages(include=['easyauth']),
    description=(
        'A simplified authentication lib based on Django and Rest Framework.'
    ),
    long_description=open('README.rst').read(),
    keywords=['Authentication', 'Django'],
    platforms=["all"],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
    # exclude_package_data={'': ['test', 'note.txt', 'manage.py', 'debug.py', 'db.sqlite3', '.gitignore', '.travis.yml']},
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt')
)

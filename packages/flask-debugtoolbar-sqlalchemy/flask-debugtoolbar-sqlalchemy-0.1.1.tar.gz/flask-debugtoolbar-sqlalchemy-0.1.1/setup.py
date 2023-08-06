#!/usr/bin/env python

import subprocess
from setuptools import setup

version = subprocess.run(['git', 'describe', '--tags'],
      stdout=subprocess.PIPE).stdout.decode().strip()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='flask-debugtoolbar-sqlalchemy',
    version=version,
    description='Flask Debug Toolbar panel for SQLAlchemy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Habunek',
    author_email='ivan@habunek.com',
    url='https://git.sr.ht/~ihabunek/flask_debugtoolbar_sqlalchemy',
    keywords='flask debug toolbar sqlalchemy panel',
    license='GPL-3',
    install_requires=[
        'flask-debugtoolbar',
        'sqlalchemy',
    ],
    packages=['flask_debugtoolbar_sqlalchemy'],
    package_data={
        'flask_debugtoolbar_sqlalchemy': [
            'templates/*.html',
        ]
    },
    classifiers=[
        'Framework :: Flask',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
    ]
)

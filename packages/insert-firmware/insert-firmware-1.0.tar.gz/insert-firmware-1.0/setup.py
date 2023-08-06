#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='insert-firmware',
    version='1.0',
    description='Add the new firmware into the database',
    author='Omar Diaz',
    author_email='diaz@autoaid.de',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'mysqlclient',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'insert_firmware = insert_firmware:main'
        ]

    },
)
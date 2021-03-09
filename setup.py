# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in niyopolymers/__init__.py
from niyopolymers import __version__ as version

setup(
	name='niyopolymers',
	version=version,
	description='IDK',
	author='Atriina',
	author_email='deverlopers@atriina.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

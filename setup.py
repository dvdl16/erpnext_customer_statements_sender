# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in erpnext_customer_statements_sender/__init__.py
from erpnext_customer_statements_sender import __version__ as version

setup(
	name='erpnext_customer_statements_sender',
	version=version,
	description='This app allows you to send out statements to your customers in bulk',
	author='Dirk van der Laarse',
	author_email='dirk@laarse.co.za',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

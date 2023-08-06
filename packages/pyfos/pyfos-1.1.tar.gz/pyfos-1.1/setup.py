#!/usr/bin/env python3
'''
Setup for pyfos
'''
from setuptools import setup, find_packages

setup(
	name='pyfos',
	version='1.1',
	description='Brocade FOS Library.',
	author='Brocade Communications Systems LLC.',
	author_email='Automation.BSN@broadcom.com',
	url='https://github.com/brocade/pyfos',
	download_url='https://github.com/brocade/pyfos/archive/pyfos1.1.0.tar.gz',
	keywords=['pyfos', 'fos'],
	classifiers=[],
	packages=find_packages(),
)

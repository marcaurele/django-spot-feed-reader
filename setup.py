# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

from spotfeedreader import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read()
f.close()

setup(
	name='django-spotfeedreader',
	version=".".join(map(str, VERSION)),
	description='Django module to read Spot feeds on findmespot.com to save them in your own database.',
	long_description=long_description,
	license='New BSD License',
	author='Marc-Aurèle Brothier',
	author_email='marc-aurele@peakxl.com',
	url='https://github.com/marcaurele/django-spotfeedreader',
	packages=find_packages(),
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'Environment :: Web Environment',
		'Topic :: System :: Archiving :: Mirroring',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Framework :: Django',
	],
)

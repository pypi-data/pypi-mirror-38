# Copyright 2018 Vitaly Burovoy <vitaly.burovoy@gmail.com>
# SPDX-License-Identifier: BSD-3-clause

from setuptools import setup

filename = 'objfreeze/__init__.py'
VERSION = None
with open(filename) as h_rd:
	for line in h_rd:
		if not line.startswith('__version__'):
			continue

		_, delim, version = line.partition('=')
		if delim:
			VERSION = version.strip(''' '"\n''')
		break

if VERSION is None:
	raise RuntimeError('unable to read the version from %r' % filename)

readme = open("README.rst").read()

setup(
	name='objfreeze',
	version=VERSION,
	packages=['objfreeze'],

	author='Vitaly Burovoy',
	author_email='vitaly.burovoy@gmail.com',
	description='Function to convert data into freezed (immutable) version',
	long_description=readme,
	url='https://gitlab.com/vitaly.burovoy/py-objfreeze',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Topic :: Software Development :: Libraries',
	],
	platforms='OS-independent',
	license='BSD',

	tests_require=[
		'flake8',
		'pylint',
	],
)

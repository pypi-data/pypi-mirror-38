#!/usr/bin/env python

import setuptools

setuptools.setup(
	name='eb2',
	version='0.0.1',
	scripts=['eb2'],
	author="Jonathas Hortense",
	author_email="jonathas.hortense@daliaresearch.com",
	description="Elastic Beanstalk ssh cli using the internal IP address",
	# long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jonathortense/homebrew-eb2",
	packages=setuptools.find_packages(),
	install_requires=[
		'awsebcli'
	],
)

#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from setuptools import setup

setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name='opensesame-plugin-Pong',
	version='0.1.2.3',
	description='Create a Pong experiment',
	author='Mark Span',
	author_email='m.m.span@rug.nl',
	url='https://github.com/markspan/Pong',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: Win32 (MS Windows)',
		'Environment :: Win32 (MS Windows)',
		'Environment :: MacOS X',
		'Environment :: Other Environment',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	#install_requires=['pylsl'],
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=[
		# First the target folder.
		('share/opensesame_plugins/Pong',
		# Then a list of files that are copied into the target folder. Make sure
		# that these files are also included by MANIFEST.in!
		[
			'Pong.md',
			'Pong.png',
			'Pong_large.png',
			'Pong.py',
			'info.yaml',
			]
		)]
	)
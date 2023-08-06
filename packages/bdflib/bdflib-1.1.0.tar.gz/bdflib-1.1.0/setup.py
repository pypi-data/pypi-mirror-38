#!/usr/bin/python
from setuptools import setup

setup(
		name='bdflib',
		version='1.1.0',
		description="Library for working with BDF font files.",
		author="Timothy Allen",
		author_email="screwtape@froup.com",
		url='https://gitlab.com/Screwtapello/bdflib/',
		packages=['bdflib', 'bdflib.test'],
		entry_points={
			'console_scripts': [
				"bdflib-embolden = bdflib.tools:embolden",
				"bdflib-fill = bdflib.tools:fill",
				"bdflib-merge = bdflib.tools:merge",
				"bdflib-passthrough = bdflib.tools:passthrough",
			]
		}
	)

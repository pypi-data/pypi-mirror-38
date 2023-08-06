#!/usr/bin/python
import os.path
from setuptools import setup

root_path = os.path.dirname(__file__)
readme_path = os.path.join(root_path, "README.md")
with open(readme_path, "r") as handle:
	long_description = handle.read()

setup(
		name='bdflib',
		version='1.1.1',
		description="Library for working with BDF font files.",
		long_description=long_description,
		long_description_content_type="text/markdown",
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

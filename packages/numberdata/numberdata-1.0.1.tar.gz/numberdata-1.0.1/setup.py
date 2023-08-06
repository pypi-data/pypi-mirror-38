import setuptools

with open("README.md","r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="numberdata",
	version="1.0.1",
	author="Anuj Mokashi",
	author_email="xyz@abc.com",
	description="A simple package calculating values for a single number",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="",
	keywords='package numbers calculations',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"Operating System :: OS Independent"
	],
	)
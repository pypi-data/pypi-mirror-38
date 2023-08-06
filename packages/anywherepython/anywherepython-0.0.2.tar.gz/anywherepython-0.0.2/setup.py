from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
		name = 'anywherepython',
		version = '0.0.2',
		author = 'Szabó Dániel Ernő',
		author_email = 'r3ap3rpy@gmail.com',
		description = 'Python library for interacting with the pythonanywhere API!',
		long_description = "This package provides a convenient way to interact with the official API, there are very few steps to set it up and after that you can schedule tasks based on this!",
		url = "https://github.com/r3ap3rpy/anywherepython",
		license = 'MIT',
		packages = ['anywherepython'],
		zip_safe = False,
		include_package_data=True,
		install_requires=[
          'requests',
      ],
      	classifiers = [
      		"Programming Language :: Python :: 3",
      		"License :: OSI Approved :: MIT License",
      		"Operating System :: OS Independent",
      	],
	)
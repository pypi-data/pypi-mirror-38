import sys
import setuptools
try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

if sys.version_info <= (2, 4):
    error = 'Requires Python Version 2.5 or above... Exiting.'

requirements = []

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name='jsonizable',
      version='0.0.5',
      description='Convert your Python classes into JSON objects easily.',
      long_description=long_description,
      scripts=[],
      url='https://github.com/pablomartinezm/jsonipy',
      packages=setuptools.find_packages(),
      license='Apache 2.0',
      platforms='Posix; MacOS X; Windows',
      long_description_content_type="text/markdown",
      setup_requires=requirements,
      install_requires=requirements,
      test_suite='googlemaps.test',
      classifiers=[
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
    )

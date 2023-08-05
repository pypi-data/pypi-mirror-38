from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='marcolibrary',
    version='0.0.6',
    description='A simple library for marcodomenichetti',
    long_description=long_description,  #this is the
    author='marco domenichetti',
    author_email='marcodomenichetti@gmail.com',
    license='MIT',
    keywords='marcodomenichetti simple privat',
    packages=["marcolibrary"],
    url='http://www.marcodomenichetti.com'

)

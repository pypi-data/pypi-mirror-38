# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='yardict',
    version='0.9.0',
    description='Fast and simple implementation of a dictionary which accepts integer '
                'ranges as keys and has O(log n) complexity for lookup.',
    url='https://github.com/danse-macabre/yardict',
    author='Maksim Malyutin',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='range dict dictionary',
    packages=find_packages(exclude=['config', 'docs', 'tests']),
    extras_require={
        'dev': ['nose'],
    }
)

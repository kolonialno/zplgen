import os
import sys

from setuptools import setup
from codecs import open
from os import path

# Publish to Pypi
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist')
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read().strip()

setup(
    name='zplgen',
    version=version,

    description='A library to aid in generating ZPL2 code.',
    long_description=long_description,

    url='https://github.com/kolonialno/zplgen',

    author='Kolonial.no',
    author_email='tech@kolonial.no',

    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Maturity
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Python versions supported
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='zpl zpl2',

    packages=['zplgen'],

    install_requires=[
        'future',
    ],
)

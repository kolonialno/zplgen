import os
import sys

from zplgen import __version__
from setuptools import setup

from codecs import open

# Publish to Pypi
if sys.argv[-1] == 'publish':
    os.system('rm -r dist/')
    os.system('python setup.py sdist')
    os.system('python setup.py bdist_wheel')
    os.system('twine upload dist/* -r pypi')
    sys.exit()

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zplgen',
    version=__version__,

    description='A library to aid in generating ZPL2 code.',
    long_description=long_description,

    url='https://github.com/kolonialno/zplgen',

    author='Kolonial.no',
    author_email='tech@kolonial.no',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Maturity
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

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

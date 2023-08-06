from setuptools import setup

DISTNAME = 'fbu'
DESCRIPTION = "PyFBU"
#VERSION = '0.0.2'
VERSION = '0.1.2'
AUTHOR = 'Davide Gerbaudo, Clement Helsens and Francesco Rubbo'
AUTHOR_EMAIL = 'clement.helsens@gmail.com'
URL = 'https://github.com/pyFBU/fbu'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Physics',
    'Operating System :: OS Independent',
    ]

required = ['pymc3']

setup(
    name=DISTNAME,
    version=VERSION,
    packages=['fbu','fbu.tests'],
    license='LICENSE.txt',
    long_description=open('README.rst','rt').read(),
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=classifiers,
    install_requires=required
    )
    
##to upload package
## python setup.py sdist
## twine upload dist/*

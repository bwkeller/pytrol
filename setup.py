#!/usr/bin/env python

from distutils.core import setup

setup( name="Pytrol", version='0.1', author='BW Keller',
        author_email='malzraa@gmail.com',
        url='https://github.com/bwkeller/pytipsy', py_modules=['pytrol'],
        license='LICENCE', long_description=open('README.md').read(),
        install_requires=[ "Numpy >= 1.5.1", "pynbody" ],)

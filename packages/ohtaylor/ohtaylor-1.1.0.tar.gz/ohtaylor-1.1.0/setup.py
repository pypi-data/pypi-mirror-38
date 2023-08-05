
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


short_description = \
    'Multi-Variate Taylor Series Approximation/Calculation Library for Python'

setup(
    name='ohtaylor',
    version='1.1.0',
    packages=['ohtaylor'],
    url='https://gitlab.com/mochan/ohtaylor',
    license='Apache 2.0',
    author='Mochan Shrestha',
    author_email='',
    description=short_description,
    long_description=read('README'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)

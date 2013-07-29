from distutils.core import setup
import os
import glob

setup(
    name = 'astroraf',
    packages = [ 'headers' ],
    url = 'https://github.com/justincely/astroraf',
    version = '0.0.1', 
    description = 'Package of Pyraf/IRAF replacement tasks',
    author = 'Justin Ely',
    author_email = 'ely@stsci.edu',
    keywords = ['astronomy'],
    classifiers = ['Programming Language :: Python',
                   'Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    requires = ['numpy','pyfits'],
    scripts =  ['scripts/hselect','scripts/hedit','scripts/imhead','scripts/show_lines',
               'scripts/imstat']
    )


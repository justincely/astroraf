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
    scripts =  ['scripts/hselect']
    )


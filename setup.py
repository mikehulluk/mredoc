 import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mredoc",
    version = "0.0.1.1-rc2",
    author = "Mike Hull",
    author_email = "mikehulluk@gmail.com",
    description = ("Tools for generation hierachical documents in HTML and PDF, primarily designed for building reports of computational models."),
    license = "BSD",
    url = "https://github.com/mikehulluk/mreorg",

    package_dir = {'':'src' },
    packages=['mredoc',
              'mredoc.util',
              'mredoc.visitors',
              'mredoc.writers',
              'mredoc.writers.html',
              'mredoc.writers.latex'
              ],
    # Could also have been done with 'scripts=':
    #entry_points = {
    #    'console_scripts': [
    #        'mreorg.curate = mreorg.curator.cmdline.mreorg_curate:main',
    #    ],
    #},

    package_data={
        'mredoc':[
            'resources/*',
            'test_data/*',
            ]
        },


    #data_files=[('mreorg/etc', ['etc/configspec.ini']),
    #            #('config', ['cfg/data.cfg']),
    #            #('/etc/init.d', ['init-script'])
    #            ],


    install_requires=['matplotlib','mredoc','pygments'],

    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

"""
MSMExplorer: Visualizations for statistical models of biomolecular dynamics
"""

import sys
import subprocess
import numpy as np
from os.path import join as pjoin
from setuptools import setup, Extension, find_packages

from distutils.spawn import find_executable
try:
    sys.dont_write_bytecode = True
    sys.path.insert(0, '.')
    from basesetup import write_version_py
finally:
    sys.dont_write_bytecode = False

try:
    import Cython
    from Cython.Distutils import build_ext

    if Cython.__version__ < '0.18':
        raise ImportError()
except ImportError:
    print(
        'Cython version 0.18 or later is required. Try "conda install cython"')
    sys.exit(1)

NAME = "msmexplorer"
VERSION = "0.2.0.dev0"
ISRELEASED = False
__version__ = VERSION


def readme_to_rst():
    pandoc = find_executable('pandoc')
    if pandoc is None:
        raise RuntimeError("Turning the readme into a description requires "
                           "pandoc.")
    long_description = subprocess.check_output(
        [pandoc, 'README.md', '-t', 'rst'])
    short_description = long_description.split('\n\n')[1]
    return {
        'description': short_description,
        'long_description': long_description,
    }


extensions = []
extensions.append(
    Extension('msmexplorer.example_datasets._muller',
              sources=[pjoin('msmexplorer', 'example_datasets', '_muller.pyx')],
              include_dirs=[np.get_include()]))


def main(**kwargs):

    write_version_py(VERSION, ISRELEASED, 'msmexplorer/version.py')

    setup(
        name=NAME,
        version=VERSION,
        description=('Visualizations for statistical models'
                     'of biomolecular dynamics.'),
        platforms=("Windows", "Linux", "Mac OS-X", "Unix",),
        classifiers=(
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Topic :: Scientific/Engineering',
        ),
        keywords=('visualizations', 'biomolecular', 'simulations',
                  'markov state models'),
        author="Carlos Xavier Hernández",
        author_email="cxh@stanford.edu",
        url='https://github.com/cxhernandez/%s' % NAME,
        download_url='https://github.com/cxhernandez/%s/tarball/master' % NAME,
        license='LGPLv2+',
        packages=find_packages(),
        include_package_data=True,
        package_data={
            NAME: ['README.md',
                   'requirements.txt'],
        },
        zip_safe=False,
        ext_modules=extensions,
        cmdclass={'build_ext': build_ext},
        **kwargs
    )


if __name__ == '__main__':
    kwargs = {}
    if any(e in sys.argv for e in ('upload', 'register', 'sdist')):
        kwargs = readme_to_rst()
    main(**kwargs)

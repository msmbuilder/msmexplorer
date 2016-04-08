"""
MSMExplorer: Visualizations for statistical models of biomolecular dynamics
"""

import sys
import subprocess

from distutils.spawn import find_executable
from setuptools import setup, find_packages
from basesetup import write_version_py

NAME = "msmexplorer"
VERSION = "0.1.0.dev0"
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


def main(**kwargs):

    write_version_py(VERSION, ISRELEASED, 'osprey/version.py')

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
        packages=[NAME] + [NAME + '.%s' % e for e in find_packages(NAME)],
        package_dir={'': NAME},
        include_package_data=True,
        package_data={
            NAME: ['README.md',
                   'requirements.txt'],
        },
        zip_safe=True,
        **kwargs
    )


if __name__ == '__main__':
    kwargs = {}
    if any(e in sys.argv for e in ('upload', 'register', 'sdist')):
        kwargs = readme_to_rst()
    main(**kwargs)

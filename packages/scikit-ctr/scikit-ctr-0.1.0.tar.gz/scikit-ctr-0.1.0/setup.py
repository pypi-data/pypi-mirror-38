#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
import sys

import setuptools
from distutils.command.build_py import build_py
from distutils.command.sdist import sdist

DISTNAME = 'scikit-ctr'

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

test_requirements = ['pytest', ]


def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True)

    config.add_subpackage('skctr')
    config.add_data_dir('skctr/data')

    return config


with open('requirements/default.txt') as fid:
    INSTALL_REQUIRES = [l.strip() for l in fid.readlines() if l]

# requirements for those browsing PyPI
REQUIRES = [r.replace('>=', ' (>= ') + ')' for r in INSTALL_REQUIRES]
REQUIRES = [r.replace('==', ' (== ') for r in REQUIRES]
REQUIRES = [r.replace('[array]', '') for r in REQUIRES]

extra = {'configuration': configuration}
if __name__ == '__main__':
    try:
        from numpy.distutils.core import setup

        extra = {'configuration': configuration}
        # Do not try and upgrade larger dependencies
        for lib in ['scikit-learn']:
            try:
                __import__(lib)
                INSTALL_REQUIRES = [i for i in INSTALL_REQUIRES if lib not in i]
            except ImportError:
                pass
    except ImportError:
        if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                   sys.argv[1] in ('--help-commands',
                                                   '--version',
                                                   'clean',
                                                   'egg_info',
                                                   'install_egg_info',
                                                   'rotate')):
            # For these actions, NumPy is not required.
            #
            # They are required to succeed without Numpy for example when
            # pip is used to install scikit-image when Numpy is not yet
            # present in the system.
            from setuptools import setup

            extra = {}
        else:
            print('To install scikit-image from source, you will need numpy.\n' +
                  'Install numpy with pip:\n' +
                  'pip install numpy\n'
                  'Or use your operating system package manager. For more\n' +
                  'details, see https://scikit-image.org/docs/stable/install.html')
            sys.exit(1)

    setup(
        name=DISTNAME,
        license="MIT license",
        long_description=readme + '\n\n' + history,
        keywords='scikit,ctr',
        author="Duo An",
        author_email='anduo@qq.com',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6'
        ],
        description="A scikit extends for Click-Through-Rate prediction.",
        entry_points={
            'console_scripts': [
                'skctr=skctr.cli:main',
            ],
        },
        install_requires=INSTALL_REQUIRES,
        #requires=REQUIRES,
        python_requires='>3.6',
        packages=setuptools.find_packages(exclude=["tests"]),
        include_package_data=True,
        test_suite='tests',
        tests_require=test_requirements,
        url='https://github.com/classtag/scikit-ctr',
        version='0.1.0',
        zip_safe=False,
        cmdclass={'build_py': build_py, 'sdist': sdist},
        **extra
    )

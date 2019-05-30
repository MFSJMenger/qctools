#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np
import os

pwd = os.path.abspath(os.path.dirname(__file__))

def ljoin(path):
    global pwd
    return os.path.join(pwd, path)


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]


cppgrep = Extension('qctools.cppgrep',
                    sources=["src/cppgrep.pyx", "src/filehandler.cpp"],
                    include_dirs=[np.get_include(), ljoin("include")],
                    language="c++",
                    extra_compile_args=['-std=c++11'],
                    extra_link_args=['-L/usr/lib/x86_64-linux-gnu/'], # in case -lpthread etc. are not found!
)


setup(
    author="Maximilian Menger",
    author_email='maximilian.menger@univie.ac.at',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python tools for quantum chemists",
    entry_points={
        'console_scripts': [
            'qctools=qctools.cli:main',
        ],
    },

    ext_modules = [cppgrep],
    cmdclass = {'build_ext': build_ext},

    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='qctools',
    name='qctools',
    packages=find_packages(include=['qctools']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/MFSJMenger/qctools',
    version='0.2.0',
    zip_safe=False,
)

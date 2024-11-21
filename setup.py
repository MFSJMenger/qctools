#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from distutils.extension import Extension
#from Cython.Distutils import build_ext
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

requirements = ['Click>=6.0', 'pycolt>=0.2' ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]


#cppgrep = Extension('qctools.cppgrep',
#                    sources=["src/cppgrep.pyx", "src/filehandler.cpp"],
#                    include_dirs=[np.get_include(), ljoin("include")],
#                    language="c++",
#                    extra_compile_args=['-std=c++11', "-O3"],
#                    extra_link_args=['-L/usr/lib/x86_64-linux-gnu/'], # in case -lpthread etc. are not found!
#)


setup(
    author="Maximilian F.S.J. Menger",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python tools for quantum chemists",
    entry_points={},

#    ext_modules = [cppgrep],
#    cmdclass = {'build_ext': build_ext},

    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='qctools',
    name='qctools',
    packages=find_packages(include=['qctools', 'qctools.*']),
    license="Apache License v2.0",
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mfsjmenger/qctools',
    version='0.3.0',
    zip_safe=False,
)

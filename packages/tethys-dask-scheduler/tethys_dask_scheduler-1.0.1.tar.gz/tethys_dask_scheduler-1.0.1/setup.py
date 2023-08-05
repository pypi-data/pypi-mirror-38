"""
********************************************************************************
* Name: setup.py
* Authors: Nathan Swain, Tran H, Teva V
* Created On: 2018
* Copyright: AQUAVEO LLC
* License: BSD 2-Clause License
********************************************************************************
"""
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requires = [
    'distributed',
]

version = '1.0.1'

setup(
    name='tethys_dask_scheduler',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='BSD 2-Clause License',
    description='A Dask scheduler with custom SchedulerPlugins to support integration with Tethys Platform',
    long_description=README,
    url='http://tethysplatform.org/',
    author='Nathan Swain',
    author_email='nswain@aquaveo.com',
    entry_points={
        'console_scripts': ['tethys-dask-scheduler=tethys_dask_scheduler.dask_scheduler:go', ],
    },
    test_suite='tests',
    install_requires=requires,
)

from setuptools import setup, find_packages
import os
import sys
from distutils.sysconfig import get_python_lib

setup(
    name='dooflask-cli',
    version='0.1a1',
    url='https://github.com/arissupriy/dooflask',
    author_email='arissy96@gmail.com',
    description='Command CLI for dooflask framework',
    author='Aris Supriyanto',
    license='MIT',
    packages=['dooflask_cli'],
    entry_points={'console_scripts': [
        'doo = dooflask_cli:doo',
    ]},
    install_requires=[
        'requests',
    ],
)

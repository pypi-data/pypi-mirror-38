import sys
import os
import subprocess
from distutils.spawn import find_executable
import setuptools
from setuptools import setup, find_packages 
from setuptools.command.build_py import build_py
from setuptools import Command

NAME = "ptcaffe-plugins"
PACKAGES = find_packages() # [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]

setup(
    name = NAME,
    version = "0.0.0.rc1",
    description = 'ptcaffe plugins',
    long_description = 'ptcaffe plugins',
    license = "MIT Licence", 
    url = "http://github.com/marvis",
    author = "xiaohang",
    author_email = "",
    packages = PACKAGES,
    #include_package_data = True,
    platforms = "any", 

    install_requires=[
        'easydict',
        'nose',      # for test 
        'packaging', # for version compare
        #'pytorch>=0.3.0',
        #'torchvision>=0.2.0',
        #'opencv-python',
        'setuptools>=16.0',
        'ptcaffe',
    ],
    scripts = [],
    #test_suite='test'
)

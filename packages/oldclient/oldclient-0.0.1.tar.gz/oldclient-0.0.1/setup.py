import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='oldclient',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A Python module for making HTTP requests to Online Linguistic'
                ' Database (OLD) instances.',
    long_description=README,
    url='http://www.onlinelinguisticdatabase.org/',
    license='Apache License 2.0',
    author='Joel Dunham',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests',
    ],
)

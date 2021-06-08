#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
   name='piemmer',
   version='1.0.5',
   description='A algorithm that simplify the input for principal component analysis',
   author='Hao-Wei Chang',
   author_email='emmer.man42@gmail.com',
   packages=find_packages(),
   license_files = 'LICENSE.txt',
   package_data={'piemmer': ['data/*.csv', 'data/*/*.csv', 'data/*/*/*.csv']},
   install_requires=['numpy', 'pandas', 'matplotlib', 'scikit-bio', 'scipy', 'tqdm', 'statsmodels'],
)

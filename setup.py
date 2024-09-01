from setuptools import setup, find_packages

setup(
    name='my_package',  # Name of your package
    version='0.1.0',  # Version of your package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'pandas', 'numpy', 'os', 'importlib', 'matplotlib.pyplot', 'external_func'
    ],
    package_data={
        '': ['*.ipynb'],  # Include Jupyter notebooks in the package
    },
    include_package_data=True,
    author='Marcin Socha',
    author_email='ms418253@students.mimuw.edu.pl',
    description='A package containing functions and a Jupyter notebook.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/marsocha/NYPD_Marcin_Socha',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

import pandas as pd
import numpy as np
import os
import importlib
import matplotlib.pyplot as plt
import external_func
importlib.reload(external_func)
import external_func as ef
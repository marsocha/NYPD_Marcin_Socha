from setuptools import setup, find_packages

setup(
    name='paczka_projekt_nazwap',
    version='0.1.0',
    author='Marcin Socha',
    author_email='ms418253@students.mimuw.edu.pl',
    description='Paczka z projektem',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/marsocha/',
    packages=find_packages(),
    install_requires=[
        'nbclient',
        'nbconvert',
        'nbformat',
        'argparse',
        'nbformat',
        'pandas',
        'numpy',
        'os',
        'importlib',
        'matplotlib.pyplot',
        'cProfile',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

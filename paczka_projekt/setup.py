from setuptools import setup, find_packages


setup(
    name='paczka_projekt',
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
    package_data={
        'paczka_projekt': ['marcin_socha_NYPD.ipynb'],  # Include the notebook in the package
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'run_notebook=your_package.run:run_notebook',  # Add a command to run the notebook
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

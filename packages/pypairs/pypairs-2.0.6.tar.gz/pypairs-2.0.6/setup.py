import setuptools
from distutils.core import setup

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypairs',
    version='2.0.6',
    packages=['pypairs'],
    url='https://github.com/rfechtner/pypairs',
    license='https://github.com/rfechtner/pypairs/blob/master/LICENSE',
    author='Ron Fechtner',
    author_email='ronfechtner@gmail.com',
    description='A Python-reimplementation of the Pairs algorithm described by A. Scialdone et al. (2015)',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3 :: Only'
                 ],
    keywords='scRNA classifier machine-learning marker pairs',
    install_requires=['numpy', 'pandas', 'numba', 'colorama'],
    project_urls={  # Optional
        'Original Paper': 'http://dx.doi.org/10.1016/j.ymeth.2015.06.021',
        'GitHub URL': 'https://github.com/rfechtner/pypairs'
    },
    extras_require={
        'plot': ['mathplotlib']
    },
    long_description=long_description
)

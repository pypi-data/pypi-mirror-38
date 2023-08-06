"""Pip installation script."""

from setuptools import find_packages, setup

setup(
    name='plotlywrap',
    version="0.1.0",
    description=('Wrapper code to generate pixel-perfect publication quality'
                 'plots with Plotly.py.'),
    author='Adam J Plowman',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'plotly>=3.4.1',
        'ipywidgets',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
)

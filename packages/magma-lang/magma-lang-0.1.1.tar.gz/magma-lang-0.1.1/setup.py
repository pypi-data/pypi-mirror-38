from setuptools import setup
import sys

setup(
    name='magma-lang',
    version='0.1.1',
    description='A circuit wiring language for programming FPGAs',
    scripts=['bin/magma'],
    packages=[
        "magma",
        "magma.frontend",
        "magma.backend",
        "magma.passes",
        "magma.simulator",
        "magma.testing"
    ],
    install_requires=[
        "colorlog",
        "astor",
        "six",
        "mako",
        "pyverilog",
        "numpy",
        "graphviz",
        "coreir==0.29a0",
        "bit_vector==0.39a0"
    ],
    python_requires='>=3.6'
)

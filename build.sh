#!/bin/bash

# Create dev virtual environment
python -m venv build_venv

# Activate venv
source build_venv/bin/activate

# Install build tools
pip install build setuptools wheel

# Build package
python -m build

# Create dist if it doesn't exist
mkdir -p dist

# Build wheel and sdist
python setup.py sdist bdist_wheel

deactivate

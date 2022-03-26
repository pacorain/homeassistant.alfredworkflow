#!/bin/zsh

set -e

# Default to python3
if [[ -z $PYTHON ]]; then
    PYTHON=python3
fi

# Make sure pip is set up
${PYTHON} -m ensurepip

# Create a temporary directory for virtualenv
mkdir -p tmp

# Use pip to install virtualenv
${PYTHON} -m pip install -t tmp virtualenv

# Use virtualenv to create a virtual environment
PYTHONPATH=${PWD}/tmp:${PYTHONPATH} ${PYTHON} -m virtualenv venv

# Delete the temp directory
rm -rf tmp

# Use virtual environment pip to upgrade itself
venv/bin/python -m pip install --upgrade pip

# Use virtual environment pip to install requirements
venv/bin/python -m pip install -r requirements.txt
#!/bin/bash

directory=$(realpath $(dirname "$0")) 

# Create a python virtual environment and install the packages.
python3 -m venv "$directory/.venv"
"$directory"/.venv/bin/python3 -m pip install -e "$directory/risk-shared" -e "$directory/risk-helper" -e "$directory/risk-engine"
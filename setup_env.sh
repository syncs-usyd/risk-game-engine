#!/bin/bash

directory=$(realpath $(dirname "$0")) 

# Create a python virtual environment and install the packages.
python3 -m venv "$directory/.venv"
"$directory"/.venv/bin/python3 -m pip install "$directory/risk-shared" "$directory/risk-helper" "$directory/risk-engine"
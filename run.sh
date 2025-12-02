#!/bin/bash
# Helper script to run N-Queens solver with the correct environment

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run python from the virtual environment
"$DIR/venv/bin/python" "$DIR/main.py" "$@"

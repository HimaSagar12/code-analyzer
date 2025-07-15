#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if a directory is provided
if [ -z "$1" ]; then
  echo "Usage: ./run.sh <path_to_python_project>"
  exit 1
fi

# Get the absolute path of the script's directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Change to the script's directory to ensure correct file access
cd "$SCRIPT_DIR"

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run the analyzer
echo "
Starting code analysis..."
python analyzer.py "$1"

echo "
Analysis finished."

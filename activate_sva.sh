#!/bin/bash
# Activate SVA virtual environment
# Usage: source activate_sva.sh

cd "$(dirname "$0")"
source sva/bin/activate
echo "✅ SVA virtual environment activated"
echo "Python: $(which python)"
echo "Python version: $(python --version)"


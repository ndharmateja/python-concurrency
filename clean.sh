#!/usr/bin/env bash

# Find and remove all __pycache__ directories recursively starting from the current directory
echo "Cleaning up __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "Done!"
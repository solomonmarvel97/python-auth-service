#!/bin/bash

# Run flake8 to report issues
echo "Running flake8..."
flake8 app

# If flake8 reports issues, proceed with autopep8 and black
if [ $? -ne 0 ]; then
    echo "Issues detected. Running autopep8 and black to fix issues..."

    # Run autopep8 to fix issues (modify with your desired flags)
    autopep8 --in-place --aggressive --aggressive --recursive app

    # Run black to format code
    black app

    echo "Reformatting completed."
else
    echo "No issues detected by flake8."
fi

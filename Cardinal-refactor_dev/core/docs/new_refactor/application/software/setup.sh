#!/bin/bash

# TEMPLATE SCRIPT, MAKE CHANGES AS NEEDED #
###########################################


# Navigate to the directory containing package.json
cd "$(dirname "$0")"

# Install dependencies using npm
npm install
# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# Navigate to the client directory
cd client

# Install dependencies using npm
npm install

# Check if the installation was successful
if [ $? -eq 0 ]; then
    echo "Client dependencies installed successfully."
else
    echo "Failed to install client dependencies. Please check the error messages above."
    exit 1
fi


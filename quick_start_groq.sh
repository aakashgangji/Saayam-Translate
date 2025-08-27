#!/bin/bash

# Quick Start Script for Groq Translation API
echo "Groq Translation API Quick Start"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 is installed"

# Install requirements
echo -e "\nInstalling Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Test Groq connection
echo -e "\nTesting Groq connection..."
python3 test_groq_connection.py

if [ $? -eq 0 ]; then
    echo "✓ Groq connection test passed"
else
    echo "✗ Groq connection test failed"
    echo "Please check your internet connection and API key"
    exit 1
fi

# Start the API
echo -e "\nStarting Translation API..."
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

python3 main.py

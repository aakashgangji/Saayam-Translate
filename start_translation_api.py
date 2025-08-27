#!/usr/bin/env python3
"""
Simple script to start the Groq Translation API
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    packages = [
        "fastapi",
        "uvicorn[standard]", 
        "requests",
        "langdetect",
        "pydantic",
        "python-multipart",
        "groq"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
            return False
    
    return True

def check_groq():
    """Check if Groq API key is valid and model is available"""
    print("Checking Groq setup...")
    
    try:
        import groq
        api_key = "XXX"  # Replace with your actual Groq API key
        groq_client = groq.Groq(api_key=api_key)
        
        # Test with a simple completion
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            temperature=0.1
        )
        
        if response and response.choices:
            print("Groq API is working and Llama 3.1 70B model is available")
            return True
        else:
            print("Groq API returned empty response")
            return False
    except Exception as e:
        print(f"Error checking Groq: {e}")
        print("Please ensure your Groq API key is valid")
        return False

def start_api():
    """Start the translation API"""
    print("Starting Translation API...")
    
    try:
        # Import and run the API
        from main import app
        import uvicorn
        
        print("Translation API started successfully!")
        print("API will be available at: http://localhost:8000")
        print("API docs at: http://localhost:8000/docs")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please install required packages first")
        return False
    except Exception as e:
        print(f"Error starting API: {e}")
        return False

def main():
    """Main function"""
    print("Groq Translation API Starter")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        import requests
        import langdetect
        import pydantic
        import groq
        print("All required packages are already installed")
    except ImportError:
        print("Some packages are missing, installing...")
        if not install_requirements():
            print("Failed to install requirements")
            return False
    
    # Check Groq
    if not check_groq():
        print("Groq setup issue")
        print("Please ensure your Groq API key is valid")
        return False
    
    # Start the API
    start_api()

if __name__ == "__main__":
    main()

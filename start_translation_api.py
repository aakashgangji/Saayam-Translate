#!/usr/bin/env python3
"""
Simple script to start the Ollama Translation API
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
        "python-multipart"
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

def check_ollama():
    """Check if Ollama is running and Mistral is available"""
    print("Checking Ollama setup...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            if "mistral" in str(model_names).lower():
                print("Ollama is running and Mistral model is available")
                return True
            else:
                print("Mistral model not found")
                return False
        else:
            print("Ollama API not responding")
            return False
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False

def start_api():
    """Start the translation API"""
    print("Starting Translation API...")
    
    try:
        # Import and run the API
        from main_ollama import app
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
    print("Ollama Translation API Starter")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        import requests
        import langdetect
        import pydantic
        print("All required packages are already installed")
    except ImportError:
        print("Some packages are missing, installing...")
        if not install_requirements():
            print("Failed to install requirements")
            return False
    
    # Check Ollama
    if not check_ollama():
        print("Ollama setup issue")
        print("Please ensure Ollama is running and Mistral model is available")
        return False
    
    # Start the API
    start_api()

if __name__ == "__main__":
    main()

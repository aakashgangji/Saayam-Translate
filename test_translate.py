#!/usr/bin/env python3
"""
Test script for the Translation API
Demonstrates proper usage of the /translate endpoint
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_translate():
    """Test the translate endpoint with various examples"""
    
    # Test cases
    test_cases = [
        {
            "text": "Hola mundo",
            "target_language": "English",
            "description": "Spanish to English"
        },
        {
            "text": "Bonjour le monde",
            "target_language": "English", 
            "description": "French to English"
        },
        {
            "text": "Hello world",
            "target_language": "Spanish",
            "description": "English to Spanish"
        },
        {
            "text": "नमस्ते दुनिया",
            "target_language": "English",
            "description": "Hindi to English"
        }
    ]
    
    print("🚀 Testing Translation API")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n Test {i}: {test_case['description']}")
        print(f"Input: {test_case['text']}")
        print(f"Target: {test_case['target_language']}")
        
        try:
            # Make POST request to /translate endpoint
            response = requests.post(
                f"{BASE_URL}/translate",
                json={
                    "text": test_case["text"],
                    "target_language": test_case["target_language"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Success!")
                print(f"Translated: {result['translated_text']}")
                print(f"Detected Language: {result['detected_language']}")
                print(f"Confidence: {result['confidence']}")
                if result.get('fallback_used'):
                    print("Fallback translator used")
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("Connection Error: Make sure the server is running on http://localhost:8000")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    print("\nTesting Health Check")
    print("-" * 30)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"API Status: {result['status']}")
            print(f"Message: {result['message']}")
        else:
            print(f"Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Server not running")

def test_supported_languages():
    """Test the supported languages endpoint"""
    print("\nTesting Supported Languages")
    print("-" * 35)
    
    try:
        response = requests.get(f"{BASE_URL}/supported-languages")
        if response.status_code == 200:
            languages = response.json()
            print(f"Supported Languages ({len(languages)}):")
            for lang in languages[:10]:  # Show first 10
                print(f"  - {lang}")
            if len(languages) > 10:
                print(f"  ... and {len(languages) - 10} more")
        else:
            print(f"Failed to get languages: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Connection Error: Server not running")

if __name__ == "__main__":
    print("Translation API Test Suite")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test supported languages
    test_supported_languages()
    
    # Test translation
    test_translate()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\n Tips:")
    print("- Make sure Ollama is running: ollama serve")
    print("- Make sure your server is running with: python main.py")
    print("- Access API docs at: http://localhost:8000/docs")

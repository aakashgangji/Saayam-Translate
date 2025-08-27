#!/usr/bin/env python3
"""
Test script to verify Groq connection and model availability
"""

import groq
import os

def test_groq_connection():
    """Test Groq connection and model availability"""
    print("Testing Groq Connection")
    print("=" * 40)
    
    try:
        # Initialize Groq client
        api_key = "XXX"  # Replace with your actual Groq API key
        groq_client = groq.Groq(api_key=api_key)
        print("Groq client initialized successfully")
        
        print("1. Testing Groq API connection...")
        
        # Test with a simple completion
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
            temperature=0.1
        )
        
        if response and response.choices:
            print("Groq API connection successful!")
            print(f"Model: llama3-70b-8192")
            print(f"Response: {response.choices[0].message.content}")
            return True
        else:
            print("Groq API returned empty response")
            return False
            
    except Exception as e:
        print(f"Groq API error: {e}")
        print("Please ensure your Groq API key is valid")
        print("If you see a 'proxies' error, try updating the Groq client: pip install --upgrade groq")
        return False

def test_translation():
    """Test a simple translation"""
    print("\n Testing Translation")
    print("-" * 30)
    
    try:
        # Initialize Groq client
        api_key = "XXX"  # Replace with your actual Groq API keyadd
        groq_client = groq.Groq(api_key=api_key)
        print("Groq client initialized for translation test")
        
        prompt = """
        You are a professional translator. Translate the following text from English to Spanish.
        
        Text to translate: "Hello world"
        
        Please provide only the translated text without any additional explanations, quotes, or formatting.
        """
        
        print("Sending translation request to Groq...")
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.1
        )
        
        if response and response.choices:
            translated_text = response.choices[0].message.content.strip()
            print(f"Translation successful!")
            print(f"Original: Hello world")
            print(f"Translated: {translated_text}")
            return True
        else:
            print("Translation failed: Empty response")
            return False
            
    except Exception as e:
        print(f"Translation error: {e}")
        return False

if __name__ == "__main__":
    print("Groq Connection Test")
    print("=" * 50)
    
    # Test connection
    if test_groq_connection():
        print("\n Groq connection successful!")
        
        # Test translation
        if test_translation():
            print("\n All tests passed! Groq is working correctly.")
            print("\n Next steps:")
            print("1. Start the translation API: python3 main.py")
            print("2. Test the API: curl http://localhost:8000/translate")
        else:
            print("\n Translation test failed")
    else:
        print("\n Groq connection failed")

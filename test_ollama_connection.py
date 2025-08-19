#!/usr/bin/env python3
"""
Test script to verify Ollama connection and model availability
"""

import requests
import json

def test_ollama_connection():
    """Test Ollama connection and model availability"""
    print("🔍 Testing Ollama Connection")
    print("=" * 40)
    
    try:
        # Test Ollama API
        print("1. Testing Ollama API...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama API is responding")
            
            # Parse models
            data = response.json()
            models = data.get("models", [])
            print(f"📋 Found {len(models)} models:")
            
            for model in models:
                name = model.get("name", "")
                size = model.get("size", 0)
                size_gb = size / (1024**3)
                print(f"   - {name} ({size_gb:.1f} GB)")
            
            # Check for Mistral
            mistral_models = [m for m in models if "mistral" in m.get("name", "").lower()]
            if mistral_models:
                print(f"✅ Found {len(mistral_models)} Mistral model(s)")
                for model in mistral_models:
                    print(f"   - {model['name']}")
                return True
            else:
                print("❌ No Mistral models found")
                return False
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama API")
        print("💡 Please ensure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_translation():
    """Test a simple translation"""
    print("\n🚀 Testing Translation")
    print("-" * 30)
    
    try:
        # Test translation with Ollama directly
        payload = {
            "model": "mistral:latest",
            "prompt": "Translate 'Hello world' to Spanish. Only provide the translation, no explanations.",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "max_tokens": 50
            }
        }
        
        print("Sending translation request to Ollama...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("response", "").strip()
            print(f"✅ Translation successful!")
            print(f"   Original: Hello world")
            print(f"   Translated: {translated_text}")
            return True
        else:
            print(f"❌ Translation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Ollama Connection Test")
    print("=" * 50)
    
    # Test connection
    if test_ollama_connection():
        print("\n✅ Ollama connection successful!")
        
        # Test translation
        if test_translation():
            print("\n🎉 All tests passed! Ollama is working correctly.")
            print("\n📋 Next steps:")
            print("1. Start the translation API: python3 main_ollama.py")
            print("2. Test the API: curl http://localhost:8000/translate")
        else:
            print("\n❌ Translation test failed")
    else:
        print("\n❌ Ollama connection failed")

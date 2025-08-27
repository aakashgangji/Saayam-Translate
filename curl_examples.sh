#!/bin/bash

# Translation API cURL Examples
# Make sure your server is running on http://localhost:8000

echo "Translation API cURL Examples"
echo "================================="

# Test 1: Spanish to English
echo -e "\n Testing Spanish to English translation:"
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola mundo", "target_language": "English"}' \
  | python3 -m json.tool

# Test 2: French to English
echo -e "\n Testing French to English translation:"
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour le monde", "target_language": "English"}' \
  | python3 -m json.tool

# Test 3: English to Spanish
echo -e "\n Testing English to Spanish translation:"
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "Spanish"}' \
  | python3 -m json.tool

# Test 4: Hindi to English
echo -e "\n Testing Hindi to English translation:"
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्ते दुनिया", "target_language": "English"}' \
  | python3 -m json.tool

# Test 5: Health check (GET request)
echo -e "\n Testing health check (GET request):"
curl -X GET "http://localhost:8000/health" \
  | python3 -m json.tool

# Test 6: Supported languages (GET request)
echo -e "\n Testing supported languages (GET request):"
curl -X GET "http://localhost:8000/supported-languages" \
  | python3 -m json.tool

# Test 7: Groq status (GET request)
echo -e "\n Testing Groq status (GET request):"
curl -X GET "http://localhost:8000/groq-status" \
  | python3 -m json.tool

echo -e "\n All tests completed!"
echo -e "\n Remember:"
echo "   - The /translate endpoint requires POST requests"
echo "   - GET requests to /translate will return 405 Method Not Allowed"
echo "   - Use GET for /health, /supported-languages, /groq-status, etc."
echo "   - Make sure your Groq API key is valid"

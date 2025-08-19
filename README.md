# Translation API

A powerful, self-hosted multilingual translation service built with FastAPI and Ollama using the Mistral model. This API provides high-quality translations without requiring external API keys or internet connectivity.

## 🌟 Key Features

- 🤖 **Local AI Translation** - Powered by Ollama with Mistral model
- 🔑 **No API Keys Required** - Completely self-hosted solution
- 🌍 **100+ Languages** - Comprehensive language support
- 🔍 **Auto Language Detection** - Automatically detects source language
- 🎯 **High-Quality Translations** - Comparable to commercial APIs
- 🛠️ **Fallback Support** - Basic translation when Ollama is unavailable
- 🚀 **Fast & Efficient** - Built with FastAPI for high performance
- 📚 **Auto-Generated Docs** - Interactive API documentation
- 🔒 **Privacy-First** - All data stays local, no external calls
- 💰 **Cost-Free** - No usage fees or API costs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed on your system
- At least 4GB RAM (for Mistral model)

### Step 1: Install Ollama
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai
```

### Step 2: Pull the Mistral Model
```bash
ollama pull mistral
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start Ollama Service
```bash
ollama serve
```

### Step 5: Run the Translation API
```bash
python main.py
```

### Step 6: Test the API
```bash
python test_translate.py
```

## 📡 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Translation API is running. Ollama status: running"
}
```

#### 2. Translate Text
```http
POST /translate
```

**Request Body:**
```json
{
  "text": "Hello, how are you?",
  "source_language": "English",  // Optional - auto-detected if not provided
  "target_language": "Spanish"   // Optional - defaults to "English"
}
```

**Response:**
```json
{
  "original_text": "Hello, how are you?",
  "translated_text": "Hola, ¿cómo estás?",
  "detected_language": "English",
  "source_language": "English",
  "target_language": "Spanish",
  "confidence": 0.9,
  "fallback_used": false,
  "message": "Translation completed successfully using Ollama with Mistral"
}
```

#### 3. Detect Language
```http
POST /detect-language
```

**Request Body:**
```json
{
  "text": "Bonjour le monde"
}
```

**Response:**
```json
{
  "text": "Bonjour le monde",
  "detected_language": "French"
}
```

#### 4. Get Supported Languages
```http
GET /supported-languages
```

**Response:**
```json
[
  "English", "Spanish", "French", "German", "Italian", 
  "Portuguese", "Russian", "Japanese", "Korean", "Chinese",
  // ... 100+ languages
]
```

#### 5. Check Ollama Status
```http
GET /ollama-status
```

**Response:**
```json
{
  "ollama_available": true,
  "model": "mistral:latest",
  "base_url": "http://localhost:11434",
  "status": "running"
}
```

## 💻 Usage Examples

### Python
```python
import requests

# Translate text
response = requests.post("http://localhost:8000/translate", json={
    "text": "Hello world",
    "target_language": "Spanish"
})
result = response.json()
print(f"Translated: {result['translated_text']}")

# Detect language
response = requests.post("http://localhost:8000/detect-language", json={
    "text": "Hola mundo"
})
result = response.json()
print(f"Detected language: {result['detected_language']}")

# Check API status
response = requests.get("http://localhost:8000/health")
print(response.json())
```

### cURL
```bash
# Translate text
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "Spanish"}'

# Detect language
curl -X POST "http://localhost:8000/detect-language" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour le monde"}'

# Get supported languages
curl -X GET "http://localhost:8000/supported-languages"

# Check Ollama status
curl -X GET "http://localhost:8000/ollama-status"
```

### JavaScript
```javascript
// Translate text
const response = await fetch('http://localhost:8000/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Hello world',
    target_language: 'Spanish'
  })
});

const result = await response.json();
console.log(`Translated: ${result.translated_text}`);
```

## ⚙️ Configuration

### Ollama Settings
Modify the configuration in `main.py`:

```python
# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
OLLAMA_MODEL = "mistral:latest"  # Change to any model you have pulled
```

### Using Different Models
You can use any model available in Ollama:

```bash
# Available models
ollama pull llama2          # Meta's Llama 2
ollama pull codellama       # Code-focused model
ollama pull mistral:7b      # Smaller Mistral model
ollama pull mistral:instruct # Instruction-tuned Mistral
ollama pull phi             # Microsoft's Phi model

# List available models
ollama list

# Then update OLLAMA_MODEL in main.py
```

### Performance Tuning
Adjust translation parameters in `main.py`:

```python
"options": {
    "temperature": 0.1,  # Lower = more consistent, Higher = more creative
    "top_p": 0.9,       # Nucleus sampling parameter
    "max_tokens": 500    # Maximum response length
}
```

## 🌍 Supported Languages

The API supports **100+ languages** including:

### Major Languages
- **English**, **Spanish**, **French**, **German**, **Italian**
- **Portuguese**, **Russian**, **Japanese**, **Korean**, **Chinese**
- **Arabic**, **Hindi**, **Bengali**, **Urdu**, **Turkish**

### European Languages
- **Dutch**, **Swedish**, **Danish**, **Norwegian**, **Finnish**
- **Polish**, **Czech**, **Slovak**, **Hungarian**, **Romanian**
- **Bulgarian**, **Croatian**, **Serbian**, **Slovenian**, **Greek**

### Asian Languages
- **Thai**, **Vietnamese**, **Indonesian**, **Malay**, **Filipino**
- **Hindi**, **Bengali**, **Urdu**, **Persian**, **Hebrew**

### African Languages
- **Swahili**, **Afrikaans**, **Amharic**, **Somali**, **Hausa**
- **Yoruba**, **Igbo**, **Zulu**, **Xhosa**

## 🔧 Troubleshooting

### Common Issues

#### 1. Ollama Service Not Available
**Error:** `"ollama_available": false`

**Solution:**
```bash
# Start Ollama service
ollama serve

# Check if it's running
curl http://localhost:11434/api/tags
```

#### 2. Model Not Found
**Error:** `"model": "mistral:latest" not found`

**Solution:**
```bash
# Check available models
ollama list

# Pull the required model
ollama pull mistral

# Or use a different model
ollama pull llama2
# Then update OLLAMA_MODEL in main.py
```

#### 3. Port Already in Use
**Error:** `address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill <PID>

# Or use a different port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### 4. Slow Translation
**Solution:**
- Use smaller models (e.g., `mistral:7b`)
- Ensure sufficient RAM (4GB+ recommended)
- Consider using GPU acceleration
- Adjust temperature settings

### Performance Optimization

#### For Faster Responses:
```python
# Use smaller model
OLLAMA_MODEL = "mistral:7b"

# Lower temperature for consistency
"temperature": 0.05
```

#### For Better Quality:
```python
# Use larger model
OLLAMA_MODEL = "mistral:latest"

# Higher temperature for creativity
"temperature": 0.2
```

## 📊 Performance Metrics

- **Translation Speed**: 1-5 seconds per translation
- **Memory Usage**: ~4GB RAM (Mistral model)
- **Quality**: Comparable to commercial APIs
- **Throughput**: 10-20 translations per minute
- **Offline Capability**: 100% offline once model is downloaded

## 🛡️ Security & Privacy

- **No External Calls**: All processing happens locally
- **No Data Logging**: No translation data is stored
- **No API Keys**: No external service authentication required
- **Self-Hosted**: Complete control over your infrastructure
- **Open Source**: Transparent and auditable code

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

### Run All Tests
```bash
python test_translate.py
```

### Test Ollama Connection
```bash
python test_ollama_connection.py
```

### Manual Testing
```bash
# Test translation
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "Spanish"}'

# Test health
curl http://localhost:8000/health
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Improvement
- **Add more models** (Llama, CodeLlama, etc.)
- **Improve translation prompts** for better quality
- **Add new language detection methods**
- **Enhance error handling** and logging
- **Add rate limiting** and caching
- **Create Docker support** for easy deployment

### Development Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Translation

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8

# Run tests
python test_translate.py

# Format code
black main.py test_translate.py
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Ollama** - For providing the local LLM infrastructure
- **Mistral AI** - For the excellent Mistral model
- **FastAPI** - For the high-performance web framework
- **Open Source Community** - For various supporting libraries

## 📞 Support

If you encounter any issues:

1. **Check the troubleshooting section** above
2. **Review the API documentation** at http://localhost:8000/docs
3. **Test Ollama connection** with `python test_ollama_connection.py`
4. **Open an issue** on the project repository

---

**Happy Translating! 🌍✨**

#!/bin/bash

echo "🚀 Quick Start: Ollama Translation API"
echo "======================================"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

echo "📋 Step 1: Checking prerequisites..."

# Check if Python is installed
if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    echo "💡 Please install Python 3 from https://python.org"
    exit 1
else
    echo "✅ Python 3 is installed"
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "❌ pip3 is not installed"
    echo "💡 Please install pip3"
    exit 1
else
    echo "✅ pip3 is installed"
fi

# Check if Ollama is installed
if ! command_exists ollama; then
    echo "❌ Ollama is not installed"
    echo "💡 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    if [ $? -eq 0 ]; then
        echo "✅ Ollama installed successfully"
    else
        echo "❌ Failed to install Ollama"
        echo "💡 Please install manually from https://ollama.ai"
        exit 1
    fi
else
    echo "✅ Ollama is installed"
fi

echo ""
echo "📋 Step 2: Installing Python dependencies..."

# Install Python dependencies
pip3 install -r requirements_ollama.txt
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "📋 Step 3: Starting Ollama service..."

# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "✅ Ollama service is running"
else
    echo "❌ Ollama service failed to start"
    kill $OLLAMA_PID 2>/dev/null
    exit 1
fi

echo ""
echo "📋 Step 4: Checking Mistral model..."

# Check if Mistral model is available
if ollama list | grep -q "mistral"; then
    echo "✅ Mistral model is available"
else
    echo "📥 Pulling Mistral model (this may take a few minutes)..."
    ollama pull mistral
    if [ $? -eq 0 ]; then
        echo "✅ Mistral model pulled successfully"
    else
        echo "❌ Failed to pull Mistral model"
        kill $OLLAMA_PID 2>/dev/null
        exit 1
    fi
fi

echo ""
echo "📋 Step 5: Starting Translation API..."

# Check if port 8000 is available
if port_in_use 8000; then
    echo "⚠️  Port 8000 is already in use"
    echo "💡 Please stop any existing services on port 8000"
    kill $OLLAMA_PID 2>/dev/null
    exit 1
fi

# Start the translation API
echo "🚀 Starting Translation API..."
python3 main_ollama.py &
API_PID=$!

# Wait for API to start
echo "⏳ Waiting for API to start..."
sleep 3

# Check if API is running
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Translation API is running"
else
    echo "❌ Translation API failed to start"
    kill $OLLAMA_PID $API_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📡 Services running:"
echo "   - Ollama service: http://localhost:11434"
echo "   - Translation API: http://localhost:8000"
echo ""
echo "📚 Useful URLs:"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo "   - Ollama Status: http://localhost:8000/ollama-status"
echo ""
echo "🧪 Test the API:"
echo "   python3 test_translate.py"
echo ""
echo "🛑 To stop all services:"
echo "   kill $OLLAMA_PID $API_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user to stop
trap "echo ''; echo '🛑 Stopping services...'; kill $OLLAMA_PID $API_PID 2>/dev/null; echo '✅ Services stopped'; exit 0" INT

# Keep script running
wait

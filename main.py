from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from langdetect import detect, LangDetectException
from typing import Optional
import logging
# Fallback translator functions
def create_fallback_response(text: str, detected_lang: str, target_lang: str) -> dict:
    """Create a fallback response when Ollama is not available."""
    # Simple fallback translations for common phrases
    fallback_translations = {
        "hello": {
            "Spanish": "hola",
            "French": "bonjour", 
            "German": "hallo",
            "Italian": "ciao",
            "Portuguese": "olá",
            "Russian": "привет",
            "Japanese": "こんにちは",
            "Korean": "안녕하세요",
            "Chinese": "你好",
            "Arabic": "مرحبا",
            "Hindi": "नमस्ते"
        },
        "thank you": {
            "Spanish": "gracias",
            "French": "merci",
            "German": "danke",
            "Italian": "grazie", 
            "Portuguese": "obrigado",
            "Russian": "спасибо",
            "Japanese": "ありがとう",
            "Korean": "감사합니다",
            "Chinese": "谢谢",
            "Arabic": "شكرا",
            "Hindi": "धन्यवाद"
        },
        "goodbye": {
            "Spanish": "adiós",
            "French": "au revoir",
            "German": "auf wiedersehen",
            "Italian": "arrivederci",
            "Portuguese": "adeus",
            "Russian": "до свидания",
            "Japanese": "さようなら",
            "Korean": "안녕히 가세요",
            "Chinese": "再见",
            "Arabic": "مع السلامة",
            "Hindi": "अलविदा"
        }
    }
    
    # Try to find a fallback translation
    text_lower = text.lower().strip()
    for phrase, translations in fallback_translations.items():
        if phrase in text_lower:
            if target_lang in translations:
                return {
                    "original_text": text,
                    "translated_text": translations[target_lang],
                    "detected_language": detected_lang,
                    "source_language": detected_lang,
                    "target_language": target_lang,
                    "confidence": 0.3,
                    "fallback_used": True,
                    "message": f"Fallback translation used for '{phrase}'"
                }
    
    # If no fallback found, return the original text with a message
    return {
        "original_text": text,
        "translated_text": text,
        "detected_language": detected_lang,
        "source_language": detected_lang,
        "target_language": target_lang,
        "confidence": 0.1,
        "fallback_used": True,
        "message": "No fallback translation available. Please ensure Ollama is running."
    }

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Translation API",
    description="A multilingual translation service using Ollama with Mistral",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral:latest"  # You can change this to any model you have pulled

# Pydantic models
class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_language: str = "English"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    detected_language: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None
    fallback_used: Optional[bool] = False
    message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

def detect_language(text: str) -> str:
    """Detect the language of the input text."""
    try:
        detected_lang = detect(text)
        # Map language codes to full names
        language_map = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi',
            'bn': 'Bengali', 'ur': 'Urdu', 'tr': 'Turkish', 'nl': 'Dutch',
            'sv': 'Swedish', 'da': 'Danish', 'no': 'Norwegian', 'fi': 'Finnish',
            'pl': 'Polish', 'cs': 'Czech', 'sk': 'Slovak', 'hu': 'Hungarian',
            'ro': 'Romanian', 'bg': 'Bulgarian', 'hr': 'Croatian', 'sr': 'Serbian',
            'sl': 'Slovenian', 'et': 'Estonian', 'lv': 'Latvian', 'lt': 'Lithuanian',
            'mt': 'Maltese', 'el': 'Greek', 'he': 'Hebrew', 'th': 'Thai',
            'vi': 'Vietnamese', 'id': 'Indonesian', 'ms': 'Malay', 'tl': 'Filipino',
            'sw': 'Swahili', 'af': 'Afrikaans', 'is': 'Icelandic', 'ga': 'Irish',
            'cy': 'Welsh', 'eu': 'Basque', 'ca': 'Catalan', 'gl': 'Galician',
            'fy': 'Frisian', 'lb': 'Luxembourgish', 'sq': 'Albanian', 'mk': 'Macedonian',
            'bs': 'Bosnian', 'me': 'Montenegrin', 'ky': 'Kyrgyz', 'kk': 'Kazakh',
            'uz': 'Uzbek', 'tk': 'Turkmen', 'tg': 'Tajik', 'mn': 'Mongolian',
            'ka': 'Georgian', 'hy': 'Armenian', 'az': 'Azerbaijani', 'ku': 'Kurdish',
            'fa': 'Persian', 'ps': 'Pashto', 'sd': 'Sindhi', 'ne': 'Nepali',
            'si': 'Sinhala', 'my': 'Burmese', 'km': 'Khmer', 'lo': 'Lao',
            'am': 'Amharic', 'ti': 'Tigrinya', 'so': 'Somali', 'ha': 'Hausa',
            'yo': 'Yoruba', 'ig': 'Igbo', 'zu': 'Zulu', 'xh': 'Xhosa',
            'st': 'Southern Sotho', 'tn': 'Tswana', 'ss': 'Swati', 've': 'Venda',
            'ts': 'Tsonga', 'nr': 'Southern Ndebele', 'sn': 'Shona', 'rw': 'Kinyarwanda',
            'lg': 'Ganda', 'ak': 'Akan', 'tw': 'Twi', 'ee': 'Ewe', 'ff': 'Fula',
            'wo': 'Wolof', 'dy': 'Dyula', 'bm': 'Bambara', 'sg': 'Sango',
            'ln': 'Lingala', 'sw': 'Swahili', 'mg': 'Malagasy', 'co': 'Corsican',
            'oc': 'Occitan', 'an': 'Aragonese', 'ast': 'Asturian', 'ext': 'Extremaduran',
            'lad': 'Ladino', 'sc': 'Sardinian', 'fur': 'Friulian', 'lld': 'Ladin',
            'rm': 'Romansh', 'vec': 'Venetian', 'lmo': 'Lombard', 'pms': 'Piedmontese',
            'eml': 'Emilian-Romagnol', 'lij': 'Ligurian', 'nap': 'Neapolitan',
            'scn': 'Sicilian', 'cal': 'Calabrian', 'srd': 'Sardinian', 'it': 'Italian'
        }
        return language_map.get(detected_lang, detected_lang.title())
    except LangDetectException:
        return "Unknown"

def check_ollama_status() -> bool:
    """Check if Ollama is running and the model is available."""
    try:
        # Check if Ollama is running
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            return False
        
        # Check if the model is available
        models = response.json().get("models", [])
        model_names = [model.get("name", "") for model in models]
        # Check for exact match or partial match (e.g., "mistral" matches "mistral:latest")
        return any(ollama_model in model_name or model_name.startswith(ollama_model.split(':')[0]) 
                  for model_name in model_names 
                  for ollama_model in [OLLAMA_MODEL])
        
    except Exception as e:
        logger.error(f"Ollama status check failed: {str(e)}")
        return False

def translate_text(text: str, source_lang: str, target_lang: str = "English") -> str:
    """Translate text using Ollama with Mistral."""
    try:
        prompt = f"""
        You are a professional translator. Translate the following text from {source_lang} to {target_lang}.
        
        Text to translate: "{text}"
        
        Please provide only the translated text without any additional explanations, quotes, or formatting.
        """
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for more consistent translations
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result.get("response", "").strip()
            
            # Clean up the response - remove quotes if present
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]
            
            if translated_text:
                return translated_text
            else:
                raise Exception("Empty response from Ollama")
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        # Return None to indicate fallback should be used
        return None

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    ollama_status = "running" if check_ollama_status() else "not available"
    return HealthResponse(
        status="healthy",
        message=f"Translation API is running. Ollama status: {ollama_status}. Use /translate endpoint to translate text."
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    ollama_status = "running" if check_ollama_status() else "not available"
    return HealthResponse(
        status="healthy",
        message=f"Translation API is running. Ollama status: {ollama_status}"
    )

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text using Ollama with Mistral.
    
    - **text**: The text to translate
    - **source_language**: Optional source language (if not provided, will be auto-detected)
    - **target_language**: Target language (defaults to English)
    """
    try:
        # Check if Ollama is available
        if not check_ollama_status():
            raise HTTPException(
                status_code=503, 
                detail="Ollama service not available. Please ensure Ollama is running and the mistral model is pulled."
            )
        
        # Detect language if not provided
        if not request.source_language:
            detected_lang = detect_language(request.text)
            source_language = detected_lang
        else:
            source_language = request.source_language
            detected_lang = source_language
        
        # Don't translate if source and target are the same
        if source_language.lower() == request.target_language.lower():
            return TranslationResponse(
                original_text=request.text,
                translated_text=request.text,
                detected_language=detected_lang,
                source_language=source_language,
                target_language=request.target_language,
                confidence=1.0,
                fallback_used=False,
                message="Source and target languages are the same"
            )
        
        # Try to translate the text with Ollama
        translated_text = translate_text(request.text, source_language, request.target_language)
        
        # If Ollama failed, use fallback
        if translated_text is None:
            fallback_response = create_fallback_response(
                request.text, detected_lang, request.target_language
            )
            return TranslationResponse(**fallback_response)
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            detected_language=detected_lang,
            source_language=source_language,
            target_language=request.target_language,
            confidence=0.9,  # Mistral typically provides high-quality translations
            fallback_used=False,
            message="Translation completed successfully using Ollama with Mistral"
        )
        
    except Exception as e:
        logger.error(f"Translation request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/detect-language")
async def detect_language_endpoint(request: TranslationRequest):
    """
    Detect the language of the input text.
    """
    try:
        detected_lang = detect_language(request.text)
        return {
            "text": request.text,
            "detected_language": detected_lang
        }
    except Exception as e:
        logger.error(f"Language detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Language detection failed: {str(e)}")

@app.get("/supported-languages")
async def get_supported_languages():
    """
    Get list of supported languages for translation.
    """
    return [
        "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian",
        "Japanese", "Korean", "Chinese", "Arabic", "Hindi", "Bengali", "Urdu",
        "Turkish", "Dutch", "Swedish", "Danish", "Norwegian", "Finnish", "Polish",
        "Czech", "Slovak", "Hungarian", "Romanian", "Bulgarian", "Croatian",
        "Serbian", "Slovenian", "Estonian", "Latvian", "Lithuanian", "Maltese",
        "Greek", "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay", "Filipino",
        "Swahili", "Afrikaans", "Icelandic", "Irish", "Welsh", "Basque", "Catalan",
        "Galician", "Frisian", "Luxembourgish", "Albanian", "Macedonian", "Bosnian",
        "Montenegrin", "Kyrgyz", "Kazakh", "Uzbek", "Turkmen", "Tajik", "Mongolian",
        "Georgian", "Armenian", "Azerbaijani", "Kurdish", "Persian", "Pashto",
        "Sindhi", "Nepali", "Sinhala", "Burmese", "Khmer", "Lao", "Amharic",
        "Tigrinya", "Somali", "Hausa", "Yoruba", "Igbo", "Zulu", "Xhosa",
        "Southern Sotho", "Tswana", "Swati", "Venda", "Tsonga", "Southern Ndebele",
        "Shona", "Kinyarwanda", "Ganda", "Akan", "Twi", "Ewe", "Fula", "Wolof",
        "Dyula", "Bambara", "Sango", "Lingala", "Malagasy", "Corsican", "Occitan",
        "Aragonese", "Asturian", "Extremaduran", "Ladino", "Sardinian", "Friulian",
        "Ladin", "Romansh", "Venetian", "Lombard", "Piedmontese", "Emilian-Romagnol",
        "Ligurian", "Neapolitan", "Sicilian", "Calabrian"
    ]

@app.get("/ollama-status")
async def check_ollama_status_endpoint():
    """
    Check Ollama service status and model availability.
    """
    try:
        is_available = check_ollama_status()
        return {
            "ollama_available": is_available,
            "model": OLLAMA_MODEL,
            "base_url": OLLAMA_BASE_URL,
            "status": "running" if is_available else "not available"
        }
    except Exception as e:
        return {
            "ollama_available": False,
            "model": OLLAMA_MODEL,
            "base_url": OLLAMA_BASE_URL,
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Translation API")
    print(f"📡 Ollama URL: {OLLAMA_BASE_URL}")
    print(f"🤖 Model: {OLLAMA_MODEL}")
    print("🌐 API will be available at: http://localhost:8000")
    print("📚 API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

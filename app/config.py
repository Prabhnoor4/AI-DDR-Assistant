import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Central configuration for the AI DDR Assistant
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # LLM models to use (not using currently)
    MODEL_EXTRACTION = "models/gemini-2.0-flash" 
    MODEL_GENERATION = "models/gemini-2.0-flash" 

    EXTRACTION_TEMPERATURE = 0.0 
    GENERATION_TEMPERATURE = 0.0  

    MAX_OUTPUT_TOKENS = 8192
    
    USE_MOCK = False
    
    # Caching settings to avoid redundant API calls
    ENABLE_CACHE = False  # Disabled to show fresh AI generation in demos
    CACHE_DIR = "data/cache"
    
    # Retry logic for handling rate limits(for gemini)
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1.0  
    MAX_RETRY_DELAY = 60.0  

    LLM_PROVIDER = "ollama" 
    
    # Ollama configuration (local LLM server)
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2"  # Can also use "mistral", "gemma2", etc.

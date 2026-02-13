import requests
from app.config import Config
from app.extraction.providers.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider (no rate limits, free)."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or Config.OLLAMA_MODEL
        self.base_url = Config.OLLAMA_BASE_URL

    def generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate content using Ollama API."""
        url = f"{self.base_url}/api/generate"
        timeout = getattr(Config, 'OLLAMA_TIMEOUT', 300)  # Default to 300 if not set
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()["response"]
            
        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"Ollama request timed out after {timeout} seconds. The model '{self.model_name}' may be too slow.\n"
                f"Suggestions:\n"
                f"  1. Try a smaller/faster model: ollama pull llama3.2:1b\n"
                f"  2. Reduce the prompt length\n"
                f"  3. Use a GPU-accelerated setup\n"
                f"  4. Switch to Gemini provider in config.py\n"
                f"  5. Increase OLLAMA_TIMEOUT in config.py"
            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Could not connect to Ollama at {self.base_url}. \n"
                f"Make sure Ollama is running and the model '{self.model_name}' is installed.\n"
                f"Install: https://ollama.ai\n"
                f"Run: ollama pull {self.model_name}"
            )
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {str(e)}")

    def get_model_name(self) -> str:
        """Get the model name for caching purposes."""
        return f"ollama:{self.model_name}"

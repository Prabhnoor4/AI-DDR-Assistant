import google.generativeai as genai
from app.config import Config
from app.extraction.providers.base_provider import BaseLLMProvider
from app.utils.retry_handler import retry_with_exponential_backoff


class GeminiProvider(BaseLLMProvider):
    """Google Gemini API provider."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(model_name)

    @retry_with_exponential_backoff(
        max_retries=Config.MAX_RETRIES,
        initial_delay=Config.INITIAL_RETRY_DELAY,
        max_delay=Config.MAX_RETRY_DELAY
    )
    def generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate content using Gemini API with retry logic."""
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.8
            }
        )
        return response.text

    def get_model_name(self) -> str:
        return self.model_name

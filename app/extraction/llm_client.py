from app.config import Config
from app.utils.cache_manager import CacheManager
from app.extraction.providers import GeminiProvider, OllamaProvider


class LLMClient:
    """Unified LLM client with caching, retry logic, and multi-provider support."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.cache = CacheManager(Config.CACHE_DIR) if Config.ENABLE_CACHE else None
        
        # Initialize provider based on configuration
        if not Config.USE_MOCK:
            self.provider = self._create_provider()
        else:
            self.provider = None

    def _create_provider(self):
        """Create the appropriate LLM provider based on configuration."""
        provider_type = Config.LLM_PROVIDER.lower()
        
        if provider_type == "gemini":
            return GeminiProvider(self.model_name)
        elif provider_type == "ollama":
            return OllamaProvider()
        else:
            raise ValueError(
                f"Unknown LLM provider: {provider_type}. "
                f"Supported: 'gemini', 'ollama'"
            )

    def generate(self, prompt: str, temperature: float) -> str:
        """Generate text with caching and retry support."""
        # Mock mode
        if Config.USE_MOCK:
            return self._mock_response(prompt)
        
        # Check cache first
        if self.cache:
            cached_response = self.cache.get(
                prompt=prompt,
                model=self.provider.get_model_name(),
                temperature=temperature
            )
            if cached_response:
                return cached_response
        
        # Generate new response
        response = self.provider.generate(
            prompt=prompt,
            temperature=temperature,
            max_tokens=Config.MAX_OUTPUT_TOKENS
        )
        
        # Cache the response
        if self.cache:
            self.cache.set(
                prompt=prompt,
                model=self.provider.get_model_name(),
                temperature=temperature,
                response=response
            )
        
        return response

    def _mock_response(self, prompt: str):
        """
        Mock response for development/testing without API calls.
        """
        # Thermal extractor
        if '"thermal_readings"' in prompt:
            return """
{
  "thermal_readings": [
    {
      "image_id": "Image_1",
      "hotspot": "32.5°C",
      "coldspot": "24.1°C"
    }
  ]
}
            """

        # Inspection extractor
        if '"areas"' in prompt and '"general_observations"' in prompt:
            return """
{
  "areas": [
    {
      "area_name": "Hall",
      "negative_findings": ["Observed dampness at skirting level"],
      "positive_findings": []
    }
  ],
  "general_observations": []
}
            """

        # DDR Builder
        if '"property_summary"' in prompt:
            return """
{
  "property_summary": "Dampness observed in Hall.",
  "area_observations": "Hall shows dampness at skirting level.",
  "root_cause": "Possible water ingress at skirting level.",
  "severity": "Moderate due to visible dampness.",
  "recommendations": "Inspect waterproofing and repair affected area.",
  "additional_notes": "Based strictly on provided structured data.",
  "missing_info": "Not Available"
}
            """

        return "{}"

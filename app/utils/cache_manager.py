import hashlib
import json
import os
from pathlib import Path
from typing import Optional


class CacheManager:
    """
    Manages caching of LLM responses to reduce API calls.
    """

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_cache_key(self, prompt: str, model: str, temperature: float) -> str:
        """
        Generate a unique cache key based on prompt, model, and temperature.
        """
        content = f"{model}:{temperature}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, model: str, temperature: float) -> Optional[str]:
        """
        Retrieve cached response if it exists.
        """
        cache_key = self._generate_cache_key(prompt, model, temperature)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"✓ Cache hit: {cache_key[:12]}...")
                    return data["response"]
            except Exception as e:
                print(f"⚠ Cache read error: {e}")
                return None

        return None

    def set(self, prompt: str, model: str, temperature: float, response: str):
        """
        Store response in cache.
        """
        cache_key = self._generate_cache_key(prompt, model, temperature)
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            data = {
                "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,
                "model": model,
                "temperature": temperature,
                "response": response
            }

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✓ Cached response: {cache_key[:12]}...")

        except Exception as e:
            print(f"⚠ Cache write error: {e}")

    def clear(self):
        """
        Clear all cached responses.
        """
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print("✓ Cache cleared")

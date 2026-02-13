import json
import re
from app.extraction.llm_client import LLMClient
from app.config import Config


class ThermalExtractor:
    #extract thermal data from thermal report

    def __init__(self):
        self.client = LLMClient(Config.MODEL_EXTRACTION)

    def extract(self, thermal_text: str) -> dict:

        prompt = f"""
You are extracting structured thermal data from a Thermal Report.

STRICT RULES:
- Extract only explicitly written temperature readings.
- Preserve temperature values exactly as written.
- Do NOT interpret.
- Do NOT conclude moisture or leakage.
- Do NOT add new facts.
- Return ONLY valid JSON.

Return format:

{{
  "thermal_readings": [
    {{
      "image_id": "",
      "hotspot": "",
      "coldspot": ""
    }}
  ]
}}

Thermal Report:
{thermal_text}
"""

        response_text = self.client.generate(
            prompt=prompt,
            temperature=Config.EXTRACTION_TEMPERATURE
        )

        return self._parse_json(response_text)

    def _parse_json(self, response_text: str) -> dict:
        #extracting json from response text

        try:
            cleaned = re.search(r"\{.*\}", response_text, re.DOTALL)
            if cleaned:
                return json.loads(cleaned.group())
            else:
                raise ValueError("No valid JSON found in response.")

        except Exception as e:
            raise RuntimeError(f"Failed to parse thermal extraction JSON: {str(e)}")

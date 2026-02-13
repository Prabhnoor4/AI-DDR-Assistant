import json
import re
from app.extraction.llm_client import LLMClient
from app.config import Config


class InspectionExtractor:
#extracts structured data from inspection report

    def __init__(self):
        self.client = LLMClient(Config.MODEL_EXTRACTION)

    def extract(self, inspection_text: str) -> dict:
        #returns structured data from inspection report
        MAX_CHARS = 20000  # safe limit

        inspection_text = inspection_text[:MAX_CHARS]
        prompt = f"""
You are extracting structured data from an Inspection Report.

CRITICAL RULES:
- Extract only explicitly stated facts
- Do NOT assume or infer anything
- Do NOT summarize
- Do NOT add new facts
- Return ONLY valid JSON - no markdown, no explanation, no comments
- Ensure all JSON is properly formatted with correct commas and brackets
- Do NOT include trailing commas before closing brackets

Return this EXACT JSON structure:

{{
  "areas": [
    {{
      "area_name": "string",
      "negative_findings": ["string"],
      "positive_findings": ["string"]
    }}
  ],
  "general_observations": ["string"]
}}

Inspection Report:
{inspection_text}

Return only the JSON object, nothing else:
"""

        response_text = self.client.generate(
            prompt=prompt,
            temperature=Config.EXTRACTION_TEMPERATURE
        )

        return self._parse_json(response_text)

    def _parse_json(self, response_text: str) -> dict:
        #returns parsed json from response text

        try:
            # Remove markdown wrappers if present
            response_text = response_text.strip()

            if response_text.startswith("```"):
                # Extract content between ``` markers
                parts = response_text.split("```")
                if len(parts) >= 3:
                    response_text = parts[1]
                    # Remove language identifier (json, JSON, etc.)
                    if response_text.startswith("json"):
                        response_text = response_text[4:].strip()
                    elif response_text.startswith("JSON"):
                        response_text = response_text[4:].strip()

            # Extract first JSON object
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if not match:
                raise ValueError("No JSON object found in response.")

            json_text = match.group()

            
            json_text = re.sub(r",\s*([}\]])", r"\1", json_text)
            
            
            json_text = json_text[:json_text.rfind("}") + 1]

            return json.loads(json_text)

        except Exception as e:
            
            print(f"\nParsing Error: {str(e)}")
            
            return {
                "areas": [],
                "general_observations": []
            }

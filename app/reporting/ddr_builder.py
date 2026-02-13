import json
import re
from app.extraction.llm_client import LLMClient
from app.config import Config

class DDRBuilder:
    # Generates the final DDR report from processed data
    
    def __init__(self):
        self.client = LLMClient(Config.MODEL_GENERATION)
    
    def build(self, normalized_data: dict, conflicts: list, missing: list) -> dict:
        # Build comprehensive prompt for DDR generation
        prompt = f"""
Generate a professional Detailed Diagnostic Report (DDR) for a property inspection.

CRITICAL RULES:
- Use ONLY the provided data below - do NOT invent facts
- If data is empty or missing, write "Not Available"
- Do NOT mention thermal readings if thermal data is empty
- Be specific and use simple language
- Explain technical terms in parentheses

Return ONLY valid JSON in this structure (ALL values must be STRINGS with \\n for line breaks):

{{
  "property_summary": "2-3 sentence overview of issues and severity based on the data",
  "area_observations": "**[Area Name]:**\\n- Finding 1\\n- Finding 2\\n\\n(Use actual area names from data)",
  "root_cause": "Likely causes based on evidence. If insufficient data, state what's missing.",
  "severity": "**Severity Level:** [Level]\\n\\n**Reasoning:**\\n- Point 1\\n- Point 2\\n- Point 3",
  "recommendations": "**Immediate Actions (1-2 days):**\\n1. Action\\n\\n**Short-term (1-2 weeks):**\\n2. Action\\n\\n**Long-term:**\\n3. Action",
  "additional_notes": "Patterns observed, further investigation needs, preventive advice",
  "missing_info": "List missing data OR write: All necessary information was available."
}}

DATA:

{normalized_data}

Conflicts: {conflicts}
Missing: {missing}

Return ONLY the JSON object. Start with {{ and end with }}.
"""
        
        # Call LLM to generate DDR
        response = self.client.generate(
            prompt=prompt,
            temperature=Config.GENERATION_TEMPERATURE
        )
        
        return self._parse_json(response)
    
    def _parse_json(self, response_text: str) -> dict:
        # Extract and parse JSON from LLM response
        try:
            # Strip whitespace
            response_text = response_text.strip()
            
            # Remove markdown code blocks if present
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            response_text = response_text.strip()
            
            # Find JSON object
            match = re.search(r'\s*(\{.*\})\s*', response_text, re.DOTALL)
            if not match:
                raise ValueError("No JSON found in response")
            
            json_text = match.group(1).strip()
            
            # Clean up trailing commas
            json_text = re.sub(r",\s*([\]}])", r"\1", json_text)
            
            return json.loads(json_text)
        
        except Exception as e:
            print("Raw DDR Response:\n", response_text)
            raise RuntimeError(f"Failed to parse DDR JSON: {str(e)}")

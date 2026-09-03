"""
openrouter_client.py
OpenRouter LLM Client with structured JSON generation, automatic model fallback,
and error handling.
"""

import os
import re
import json
import requests
from typing import Dict, Any, Optional

def load_env():
    """Load .env file if present."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

load_env()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
FALLBACK_MODEL = os.getenv("OPENROUTER_FALLBACK_MODEL", "meta-llama/llama-3.3-70b-instruct:free")


class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        if not self.api_key:
            print("[OpenRouterClient] Warning: OPENROUTER_API_KEY not found. Operating in local fallback mode.")

    def generate_json(self, prompt: str, system_prompt: str = "", model: str = None) -> Optional[Dict[str, Any]]:
        """
        Calls OpenRouter and enforces strict JSON output parsing.
        Attempts primary model first, falls back to fallback model on failure.
        """
        if not self.api_key:
            return None

        primary_model = model or DEFAULT_MODEL
        models_to_try = [primary_model, FALLBACK_MODEL]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "NEXUS Criminal Network Analysis",
            "Content-Type": "application/json"
        }

        for chosen_model in models_to_try:
            payload = {
                "model": chosen_model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt or "You are an expert Law Enforcement Intelligence Analyst. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.1,
                "max_tokens": 1500
            }

            try:
                response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=6)
                if response.status_code == 200:
                    data = response.json()
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if content:
                        content = content.strip()
                        # Extract first JSON object match if mixed with text
                        match = re.search(r"\{[\s\S]*\}", content)
                        if match:
                            return json.loads(match.group(0))
                        return json.loads(content)
                else:
                    print(f"[OpenRouterClient] HTTP {response.status_code} on {chosen_model}")
            except Exception as e:
                pass

        return None


# Global singleton client
llm_client = OpenRouterClient()

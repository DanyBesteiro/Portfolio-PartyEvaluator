from django.conf import settings
from openai import OpenAI
import logging


import re
import json

class OpenRouterService:
    logger = logging.getLogger(__name__)

    def chat(self, messages: list, tokens=1500) -> dict:
        client = OpenAI(
            base_url=settings.OPENROUTER_API_URL,
            api_key=settings.OPENROUTER_API_KEY,
        )
        
        try:
            
            completion = client.chat.completions.create(
                model=settings.OPENROUTER_MODEL, 
                messages=messages,
                max_tokens=tokens
            )
            
            if "error" in completion:
                raise RuntimeError(
                    f"Model error: "
                    f"{completion.error.get('code')} - "
                    f"{completion.error.get('message')}"
                )

            if not completion.choices:
                raise RuntimeError("Party validator not available - Model returned no choices")
            
            return self.clean_content_response(completion.choices[0].message.content)

        except Exception as e:
            self.logger.error(f"Error en la petición: {e}")
            raise NameError("WebValidationError: " + str(e))

    def clean_content_response(self, content: str) -> dict:
        try:
            if content is None:
                return {"result": False, "confidence": 0, "error": "Error en la consulta"}
            
            content = content.strip()

            if content.startswith("```"):
                content = re.sub(r"^```(?:json)?\s*", "", content)
                content = re.sub(r"\s*```$", "", content)

            return json.loads(content)
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing AI response JSON: {e}. Response: {content}")
            return {"result": False, "confidence": 0, "error": "JSON corrupto"}
        
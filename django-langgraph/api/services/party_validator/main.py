import os
import yaml

from django.conf import settings
from django.http import JsonResponse
from ..openrouter.main import OpenRouterService

class PartyValidatorService:

    def validate(self, candidature: dict) -> dict:
        message = get_prompt_message(candidature)
        result = OpenRouterService().chat(message)
        
        return JsonResponse({"result": result}, status=200)

    
def get_prompt_message(candidature: dict)-> dict:
    prompt_templates = load_prompt('party_validation_prompts', 'party_validation')
    if not prompt_templates:
        raise ValueError("No se pudo cargar el prompt desde el archivo YAML")

    system_content = prompt_templates['system']
    user_content = prompt_templates['user'].format(
        candidature_name=candidature['name'],
        candidature_acronym=candidature['acronym']
    )

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def load_prompt(domain: str, prompt_name: str) -> dict:
    prompt_path = os.path.join(
        settings.BASE_DIR, 
        'api', 'services', 'party_validator', 'prompts', f'{domain}.yaml'
    )
    
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
        
    return prompts.get(prompt_name, {})
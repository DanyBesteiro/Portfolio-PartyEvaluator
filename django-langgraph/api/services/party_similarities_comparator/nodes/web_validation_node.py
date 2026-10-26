import os
import yaml
import logging
import json
logger = logging.getLogger(__name__)

from django.conf import settings
from ..state import PartyResolutionState
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class PartyValidationResult(BaseModel):
    candidature_id: str
    result: bool
    confidence: int = Field(ge=0, le=100)
    similarity_id: str | None

class PartyValidationResponse(BaseModel):
    results: list[PartyValidationResult]


def web_validation(state: PartyResolutionState) -> dict:

    return {"web_validation": validate_list(
        generate_list(state["coincidences"])
    )}

def generate_list(coincidences) -> list:
    list = []
    for coincidence in coincidences:
        candidate = {
            "candidature": {
                "id": coincidence["candidature"]["id"],
                "name": coincidence["candidature"]["name"],
                "acronym": coincidence["candidature"]["formatted_acronym"]
            },
            "similarities": []   
        }
        similarities = sorted(coincidence["party_similarities"], key=lambda p: p["score_ag"], reverse=True)
        for similarity in similarities: 
            if is_candidate(similarity):
                candidate["similarities"].append({
                    "id": similarity["id"],
                    "name": similarity["normalized_name"],
                    "acronym": similarity["normalized_acronym"]
                }) 

        list.append(candidate)

    return list

def is_candidate(similarity) -> bool:
    return similarity['score_ag']  >= 0.90 or similarity['score_name']  >= 0.90 or similarity['score_acro']  >= 0.90

def validate_list(list):
    prompt_templates = load_prompt('validation_prompts', 'party_geographical_validation')
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_templates["system"]),
        ("user", prompt_templates["user"])
    ])
    
    openrouterAI = ChatOpenRouter(model="openrouter/free", temperature=0.1, max_tokens=10000)
    structured_model = openrouterAI.with_structured_output(PartyValidationResponse)
    serialized_list = json.dumps(
        list,
        ensure_ascii=False,
        indent=2
    )
    
    chain = prompt | structured_model
    
    return chain.invoke({"candidatures": serialized_list})

def load_prompt(domain: str, prompt_name: str) -> dict:
    prompt_path = os.path.join(
        settings.BASE_DIR, 
        'api', 'services', 'party_similarities_comparator', 'prompts', f'{domain}.yaml'
    )
    
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
        
    return prompts.get(prompt_name, {})
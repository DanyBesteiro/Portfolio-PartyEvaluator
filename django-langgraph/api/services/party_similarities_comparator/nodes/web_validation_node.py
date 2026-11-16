import os
import yaml
import logging
import json

from django.conf import settings
from ..state import PartyResolutionState

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
class PartyValidationResult(BaseModel):
    candidature_id: str
    result: bool
    confidence: int = Field(ge=0, le=100)    
    similarity_id: str | None
    reason: str

class PartyValidationResponse(BaseModel):
    results: list[PartyValidationResult]

def web_validation(state: PartyResolutionState) -> dict:
    element_generated = RunnableLambda(generate_element)
    element_evaluated = RunnableLambda(validate_element)
    chain = element_generated | element_evaluated
    
    result = chain.batch(state["coincidences"])
    
    return {"web_validation": result}

def generate_element(coincidence) -> dict:
    return {
        "candidature": {
            "id": coincidence["candidature"]["id"],
            "name": coincidence["candidature"]["name"],
            "acronym": coincidence["candidature"]["formatted_acronym"]
        },
        "similarities": sorted(coincidence["similarities"], key=lambda p: p["score_ag"], reverse=True)
    }

def validate_element(element):
    prompt_templates = load_prompt('validation_prompts', 'party_geographical_validation')
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_templates["system"]),
        ("user", prompt_templates["user"])
    ])
    openrouterAI = ChatOpenRouter(model= settings.OPENROUTER_MODEL, temperature=0.1, max_tokens=10000)

    structured_model = openrouterAI.with_structured_output(PartyValidationResult)
    
    chain = prompt | structured_model
    return chain.invoke({'candidature' : element})
    
def is_candidate(similarity) -> bool:
    return similarity['score_ag']  >= 0.90 or similarity['score_name']  >= 0.90 or similarity['score_acro']  >= 0.90

def validate_list(list):
    prompt_templates = load_prompt('validation_prompts', 'party_geographical_validation')
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_templates["system"]),
        ("user", prompt_templates["user"])
    ])
    
    openrouterAI = ChatOpenRouter(model= settings.OPENROUTER_MODEL, temperature=0.1, max_tokens=10000)
    structured_model = openrouterAI.with_structured_output(PartyValidationResponse)
    serialized_list = json.dumps(
        list,
        ensure_ascii=False,
        indent=2
    )
    
    chain = prompt | structured_model

    return chain.batch({"candidatures": serialized_list}, return_exceptions=True)

def load_prompt(domain: str, prompt_name: str) -> dict:
    prompt_path = os.path.join(
        settings.BASE_DIR, 
        'api', 'services', 'party_similarities_comparator', 'prompts', f'{domain}.yaml'
    )
    
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
        
    return prompts.get(prompt_name, {})
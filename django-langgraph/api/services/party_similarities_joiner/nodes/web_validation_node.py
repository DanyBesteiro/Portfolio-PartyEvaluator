import os
import yaml
import logging

from django.conf import settings
from ..state import PartySimilaritiesState

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
class PartySimilarityResult(BaseModel):
    partyId1: str
    partyId2: str
    result: bool
    confidence: int = Field(ge=0, le=100)

def web_validation(state: PartySimilaritiesState) -> dict:
    main = state["similarities"]
    element = {}
    result = state["result"]

    for similarity in state["filtered_similarities"]:
        element = generate_element(main, similarity)
        validated = validate_element(element)
        
        result.append(validated.model_dump())

    return {"result": result}

def generate_element(main, similarity) -> dict:
    return {
        "partyId1": main["id"],
        "partyName1": main["name"],
        "partyAcronym1": main["acronym"],
        "partyId2": similarity["id"],
        "partyName2": similarity["name"],
        "partyAcronym2": similarity["acronym"],
    }

def validate_element(element):    
    prompt_templates = load_prompt('validation_prompts', 'party_nomenclature_validation')

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_templates["system"]),
        ("user", prompt_templates["user"])
    ])
    openrouterAI = ChatOpenRouter(
        model= settings.OPENROUTER_MODEL, 
        temperature=0.1, 
        max_tokens=5000,
        reasoning={
            "effort": "low"
        }
    )
    structured_model = openrouterAI.with_structured_output(PartySimilarityResult)
    chain = prompt | structured_model
    try:
        validated = chain.invoke({'partys': element})
        
        if validated is None:
            raise ValueError(f"LLM returned None for element: {element}")
        return validated
    except Exception as e:
        raise RuntimeError(f"Error validating party nomenclature: {e}") from e
    
def load_prompt(domain: str, prompt_name: str) -> dict:
    prompt_path = os.path.join(
        settings.BASE_DIR, 
        'api', 'services', 'party_similarities_joiner', 'prompts', f'{domain}.yaml'
    )
    
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
        
    return prompts.get(prompt_name, {})
import logging

from django.conf import settings
from ..state import PartyResolutionState
from ....infrastructure.llm.prompt_loader import load_prompt

from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
class PartyValidationResult(BaseModel):
    candidature_id: str
    result: bool
    confidence: int = Field(ge=0, le=100)    
    similarity_id: str | None
    reason: str

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

def validate_element(element) -> PartyValidationResult:
    prompt_templates = load_prompt('party_similarities_comparator', 'validation_prompts', 'party_geographical_validation')
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_templates["system"]),
        ("user", prompt_templates["user"])
    ])
    openrouterAI = ChatOpenRouter(model= settings.OPENROUTER_MODEL, temperature=0.1, max_tokens=10000)

    structured_model = openrouterAI.with_structured_output(PartyValidationResult, method="json_schema")
    
    chain = prompt | structured_model
    return chain.invoke({'coincidence' : element})
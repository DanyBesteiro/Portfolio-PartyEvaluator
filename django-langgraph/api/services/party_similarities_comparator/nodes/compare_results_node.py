from ..state import PartyResolutionState
import logging

logger = logging.getLogger(__name__)

def compare_results(state: PartyResolutionState) -> dict:
    try: 
        out = {
            "results": []
        }
        language_match = state.get("language_match")        
        web_match = state.get("web_validation")
        
        for match in web_match.results:        
            if match.candidature_id in language_match:
                aux = validate_match(language_match[match.candidature_id], match)
                out["results"].append(aux)
        
    except Exception as e: 
        logger.error(f"Error inesperado comparando resultados: {e}")

    return out

def validate_match(language_match, web_match):
    
    validation_match = False
    matched_party_id = None
    confidence = 100

    if language_match['safe_match_parties']['id'] == web_match.similarity_id or web_match.confidence>90:
        validation_match = True
        matched_party_id = web_match.similarity_id
        confidence = web_match.confidence

    return {
        "candidature_id": web_match.candidature_id,
        "validation_match": validation_match,
        "matched_party_id": matched_party_id,
        "confidence": confidence
    }
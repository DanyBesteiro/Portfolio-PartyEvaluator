from ..state import PartyResolutionState
import logging

logger = logging.getLogger(__name__)

def compare_results(state: PartyResolutionState) -> dict:
    out = {
        "results": []
    }
    language_match = state.get("language_match")
    web_match = state.get("web_validation")

    for match in web_match:
        if match.candidature_id in language_match:
            aux = validate_match(language_match[match.candidature_id], match)
            out["results"].append(aux)
    
    return out

def validate_match(language_match: dict, web_match: dict) -> dict:
    out = {
        "candidature_id": web_match.candidature_id,
        "validation_match": False,
        "matched_party_id": None,
        "reason": web_match.reason,
        "confidence": 100
    }
    
    if not language_match['safe_match_found'] and not web_match.result:
        return out

    if language_match['safe_match_parties']['id'] == web_match.similarity_id or web_match.confidence>90:
        out["validation_match"] = True
        out["matched_party_id"] = web_match.similarity_id
        out["reason"] = web_match.reason
        out["confidence"] = web_match.confidence

    return out
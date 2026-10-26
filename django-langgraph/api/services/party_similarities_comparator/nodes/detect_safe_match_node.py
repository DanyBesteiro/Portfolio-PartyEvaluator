from ..state import PartyResolutionState

def detect_safe_match(state: PartyResolutionState) -> dict:

    out = {
        "language_match": {}
    }
    
    for coincidence in state["coincidences"]:
        similarities = sorted(coincidence["party_similarities"], key=lambda p: p["score_ag"], reverse=True)

        out["language_match"][coincidence['candidature']['id']] = {
            'safe_match_found': False,
            'safe_match_parties': None
        }

        for similarity in similarities: 
            if similarity['score_ag']  >= 0.95 or similarity['score_name']  >= 0.95 or similarity['score_acro']  >= 0.95:
                out["language_match"][coincidence['candidature']['id']] = {
                    'safe_match_found': True,
                    'safe_match_parties': similarity
                }
                
    return out
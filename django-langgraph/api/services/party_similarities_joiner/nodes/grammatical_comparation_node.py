import json
import logging
import re
import unicodedata

from ..state import PartySimilaritiesState
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

STOPWORDS = {
    "de", "del", "la", "las", "el", "los",
    "y", "en", "municipio", "municipal",
    "agrupacion", "agrupaciones",
    "electores", "electoral", "electorales",
    "candidatura", "candidaturas",
    "independiente", "independientes",
    "partido", "partidos",
}

def filter_similarities(state: PartySimilaritiesState) -> dict:
    similarities = state["similarities"]

    relevant_candidates = []
    discarded = []

    for candidate in similarities.get("similarities", []):      
        if not has_obvious_lexical_difference(
            similarities['name'],
            candidate.get("name", ""),
            candidate.get("nameSimilarity", 0)
        ):
            relevant_candidates.append(candidate)
        else:
            discarded.append({
                "partyId1": similarities['id'],
                "partyId2": candidate['id'],
                "result": False,
                "confidence": 35
            })

    return {
        "filtered_similarities": relevant_candidates,
        "result": discarded
    }

def normalize_tokens(name: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", name)
    normalized = "".join(
        char for char in normalized
        if not unicodedata.combining(char)
    )

    tokens = re.findall(r"[a-z0-9]+", normalized.lower())

    return {
            token for token in tokens
            if token not in STOPWORDS
            }


def has_obvious_lexical_difference(
    original_name: str,
    candidate_name: str,
    name_similarity: float,
) -> bool:
    original_tokens = normalize_tokens(original_name)
    candidate_tokens = normalize_tokens(candidate_name)

    if not original_tokens or not candidate_tokens:
        return False

    if original_tokens.intersection(candidate_tokens):
        return False

    original = " ".join(sorted(original_tokens))
    candidate = " ".join(sorted(candidate_tokens))

    lexical_similarity = fuzz.ratio(original, candidate)

    return (
        lexical_similarity < 35
        and name_similarity < 0.65
    )
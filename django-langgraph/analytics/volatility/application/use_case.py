from ..domain.models import ElectionResult, PartyVote, VolatilityResult
from ..domain.services import PedersenVolatilityCalculator

class CalculatePedersenVolatilityUseCase:
    def __init__(self, calculator: PedersenVolatilityCalculator):
        self._calculator = calculator

    def execute(self, raw_elections: list[dict]) -> list[VolatilityResult]:
        elections = [
            ElectionResult(
                election_id=e["election_id"],
                year=e["year"],
                valid_votes=e["valid_votes"],
                parties=tuple(
                    PartyVote(party_id=p["party_id"], votes=p["votes"])
                    for p in e["parties"]
                ),
            )
            for e in raw_elections
        ]
        return self._calculator.calculate_series(elections)

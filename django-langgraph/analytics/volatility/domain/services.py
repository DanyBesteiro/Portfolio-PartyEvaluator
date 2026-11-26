from .models import ElectionResult, VolatilityResult

class PedersenVolatilityCalculator:
    @staticmethod
    def calculate_series(elections: list[ElectionResult]) -> list[VolatilityResult]:
        if len(elections) < 2:
            raise ValueError("Se necesitan al menos dos elecciones para calcular la volatilidad.")

        # Ordenamos cronológicamente para asegurar comparaciones consecutivas válidas
        sorted_elections = sorted(elections, key=lambda e: e.year)
        results: list[VolatilityResult] = []

        for prev_election, curr_election in zip(sorted_elections, sorted_elections[1:]):
            index = PedersenVolatilityCalculator._calculate_pair(prev_election, curr_election)
            results.append(
                VolatilityResult(
                    from_election_id=prev_election.election_id,
                    to_election_id=curr_election.election_id,
                    from_year=prev_election.year,
                    to_year=curr_election.year,
                    volatility_index=round(index, 2),
                )
            )
        return results

    @staticmethod
    def _calculate_pair(prev_election: ElectionResult, curr_election: ElectionResult) -> float:
        prev_shares = prev_election.get_vote_percentages()
        curr_shares = curr_election.get_vote_percentages()

        all_parties = set(prev_shares.keys()) | set(curr_shares.keys())
        
        total_abs_diff = sum(
            abs(curr_shares.get(party, 0.0) - prev_shares.get(party, 0.0))
            for party in all_parties
        )
        return 0.5 * total_abs_diff

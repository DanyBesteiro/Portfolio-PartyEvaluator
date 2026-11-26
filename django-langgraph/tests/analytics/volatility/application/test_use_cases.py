import unittest
from analytics.volatility.application.use_case import CalculatePedersenVolatilityUseCase
from analytics.volatility.domain.services import PedersenVolatilityCalculator


class TestCalculatePedersenVolatilityUseCase(unittest.TestCase):
    def test_executes_use_case_with_raw_dicts(self):
        raw_elections = [
            {
                "election_id": "election-2015",
                "year": 2015,
                "valid_votes": 10000,
                "parties": [
                    {"party_id": "party-a", "votes": 4000},
                    {"party_id": "party-b", "votes": 6000},
                ],
            },
            {
                "election_id": "election-2019",
                "year": 2019,
                "valid_votes": 10000,
                "parties": [
                    {"party_id": "party-a", "votes": 5000},
                    {"party_id": "party-b", "votes": 5000},
                ],
            },
        ]

        use_case = CalculatePedersenVolatilityUseCase(
            calculator=PedersenVolatilityCalculator()
        )
        results = use_case.execute(raw_elections)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].volatility_index, 10.0)


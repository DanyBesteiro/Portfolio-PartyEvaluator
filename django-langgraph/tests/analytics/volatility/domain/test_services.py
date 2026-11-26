import unittest
from analytics.volatility.domain.models import ElectionResult, PartyVote
from analytics.volatility.domain.services import PedersenVolatilityCalculator


class TestPedersenVolatilityCalculator(unittest.TestCase):
    def test_calculates_volatility_series_including_new_parties(self):
        e2015 = ElectionResult(
            election_id="election-2015",
            year=2015,
            valid_votes=10000,
            parties=(
                PartyVote("party-a", 4000),
                PartyVote("party-b", 3000),
                PartyVote("party-c", 3000),
            ),
        )
        e2019 = ElectionResult(
            election_id="election-2019",
            year=2019,
            valid_votes=10000,
            parties=(
                PartyVote("party-a", 3500),
                PartyVote("party-b", 3500),
                PartyVote("party-c", 3000),
            ),
        )
        e2026 = ElectionResult(
            election_id="election-2026",
            year=2026,
            valid_votes=10000,
            parties=(
                PartyVote("party-a", 3000),
                PartyVote("party-b", 4000),
                PartyVote("party-c", 2000),
                PartyVote("party-d", 1000),
            ),
        )

        results = PedersenVolatilityCalculator.calculate_series([e2026, e2015, e2019])
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].from_election_id, "election-2015")
        self.assertEqual(results[0].to_election_id, "election-2019")
        self.assertEqual(results[0].volatility_index, 5.0)

        self.assertEqual(results[1].from_election_id, "election-2019")
        self.assertEqual(results[1].to_election_id, "election-2026")
        self.assertEqual(results[1].volatility_index, 15.0)

    def test_zero_volatility_when_vote_shares_are_identical(self):
        e1 = ElectionResult("e1", 2015, 1000, (PartyVote("p1", 600), PartyVote("p2", 400)))
        e2 = ElectionResult("e2", 2019, 2000, (PartyVote("p1", 1200), PartyVote("p2", 800)))

        results = PedersenVolatilityCalculator.calculate_series([e1, e2])
        self.assertEqual(results[0].volatility_index, 0.0)

    def test_maximum_volatility_when_all_parties_are_replaced(self):
        e1 = ElectionResult("e1", 2015, 1000, (PartyVote("old-party", 1000),))
        e2 = ElectionResult("e2", 2019, 1000, (PartyVote("new-party", 1000),))

        results = PedersenVolatilityCalculator.calculate_series([e1, e2])
        self.assertEqual(results[0].volatility_index, 100.0)

    def test_raises_error_with_fewer_than_two_elections(self):
        e1 = ElectionResult("e1", 2015, 1000, (PartyVote("p1", 1000),))

        with self.assertRaisesRegex(ValueError, "al menos dos elecciones"):
            PedersenVolatilityCalculator.calculate_series([e1])

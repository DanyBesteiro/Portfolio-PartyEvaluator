import unittest
from analytics.volatility.domain.models import ElectionResult, PartyVote


class TestPartyVote(unittest.TestCase):
    def test_creates_valid_party_vote(self):
        party = PartyVote(party_id="party-a", votes=4000)
        self.assertEqual(party.party_id, "party-a")
        self.assertEqual(party.votes, 4000)

    def test_raises_error_when_votes_are_negative(self):
        with self.assertRaisesRegex(ValueError, "no pueden ser negativos"):
            PartyVote(party_id="party-a", votes=-1)


class TestElectionResult(unittest.TestCase):
    def test_calculates_vote_percentages_correctly(self):
        election = ElectionResult(
            election_id="election-2015",
            year=2015,
            valid_votes=10000,
            parties=(
                PartyVote(party_id="party-a", votes=4000),
                PartyVote(party_id="party-b", votes=3500),
            ),
        )
        self.assertEqual(
            election.get_vote_percentages(),
            {"party-a": 40.0, "party-b": 35.0},
        )

    def test_raises_error_when_valid_votes_is_zero_or_negative(self):
        with self.assertRaisesRegex(ValueError, "mayor a 0"):
            ElectionResult(
                election_id="election-2015",
                year=2015,
                valid_votes=0,
                parties=(PartyVote(party_id="party-a", votes=0),),
            )

    def test_raises_error_when_party_votes_exceed_valid_votes(self):
        with self.assertRaisesRegex(ValueError, "supera los votos válidos"):
            ElectionResult(
                election_id="election-2015",
                year=2015,
                valid_votes=1000,
                parties=(
                    PartyVote(party_id="party-a", votes=600),
                    PartyVote(party_id="party-b", votes=500),
                ),
            )

from dataclasses import dataclass

@dataclass(frozen=True)
class PartyVote:
    party_id: str
    votes: int

    def __post_init__(self):
        if self.votes < 0:
            raise ValueError(f"Los votos para {self.party_id} no pueden ser negativos.")

@dataclass(frozen=True)
class ElectionResult:
    election_id: str
    year: int
    valid_votes: int
    parties: tuple[PartyVote, ...]

    def __post_init__(self):
        if self.valid_votes <= 0:
            raise ValueError("El total de votos válidos debe ser mayor a 0.")
        total_party_votes = sum(p.votes for p in self.parties)
        if total_party_votes > self.valid_votes:
            raise ValueError(f"La suma de votos de partidos supera los votos válidos en {self.election_id}.")

    def get_vote_percentages(self) -> dict[str, float]:
        return {
            party.party_id: (party.votes / self.valid_votes) * 100
            for party in self.parties
        }

@dataclass(frozen=True)
class VolatilityResult:
    from_election_id: str
    to_election_id: str
    from_year: int
    to_year: int
    volatility_index: float

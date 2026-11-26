from django.test import override_settings
from rest_framework import status
from rest_framework.test import APISimpleTestCase


@override_settings(DJANGO_API_TOKEN="test-valid-token")
class TestPedersenVolatilityEndpoint(APISimpleTestCase):
    def setUp(self):
        self.url = "/api/analytics/volatility/"
        self.valid_payload = {
            "elections": [
                {
                    "election_id": "election-2015",
                    "year": 2015,
                    "valid_votes": 10000,
                    "parties": [
                        {"party_id": "party-a", "votes": 4000},
                        {"party_id": "party-b", "votes": 3000},
                        {"party_id": "party-c", "votes": 3000},
                    ],
                },
                {
                    "election_id": "election-2019",
                    "year": 2019,
                    "valid_votes": 10000,
                    "parties": [
                        {"party_id": "party-a", "votes": 3500},
                        {"party_id": "party-b", "votes": 3500},
                        {"party_id": "party-c", "votes": 3000},
                    ],
                },
                {
                    "election_id": "election-2026",
                    "year": 2026,
                    "valid_votes": 10000,
                    "parties": [
                        {"party_id": "party-a", "votes": 3000},
                        {"party_id": "party-b", "votes": 4000},
                        {"party_id": "party-c", "votes": 2000},
                        {"party_id": "party-d", "votes": 1000},
                    ],
                },
            ]
        }

        self.auth_headers = {"HTTP_AUTHORIZATION": "Bearer test-valid-token"}

    def test_returns_401_when_no_auth_headers_provided(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "No autorizado"})

    def test_returns_200_and_volatility_series_for_valid_payload(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format="json",
            **self.auth_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "volatility_series": [
                    {
                        "from_election_id": "election-2015",
                        "to_election_id": "election-2019",
                        "from_year": 2015,
                        "to_year": 2019,
                        "volatility_index": 5.0,
                    },
                    {
                        "from_election_id": "election-2019",
                        "to_election_id": "election-2026",
                        "from_year": 2019,
                        "to_year": 2026,
                        "volatility_index": 15.0,
                    },
                ]
            },
        )

    def test_returns_400_when_less_than_two_elections_sent(self):
        invalid_payload = {"elections": [self.valid_payload["elections"]]}

        response = self.client.post(
            self.url,
            data=invalid_payload,
            format="json",
            **self.auth_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("elections", response.data)

    def test_returns_400_when_party_votes_exceed_valid_votes(self):
        invalid_payload = {
            "elections": [
                {
                    "election_id": "election-2015",
                    "year": 2015,
                    "valid_votes": 100,
                    "parties": [{"party_id": "party-a", "votes": 150}],
                },
                {
                    "election_id": "election-2019",
                    "year": 2019,
                    "valid_votes": 100,
                    "parties": [{"party_id": "party-a", "votes": 100}],
                },
            ]
        }

        response = self.client.post(
            self.url,
            data=invalid_payload,
            format="json",
            **self.auth_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

from rest_framework import serializers

class PartyVoteInputSerializer(serializers.Serializer):
    party_id = serializers.CharField(max_length=100)
    votes = serializers.IntegerField(min_value=0)

class ElectionInputSerializer(serializers.Serializer):
    election_id = serializers.CharField(max_length=100)
    year = serializers.IntegerField(min_value=1800, max_value=2100)
    valid_votes = serializers.IntegerField(min_value=1)
    parties = PartyVoteInputSerializer(many=True, allow_empty=False)

class VolatilityCalculationRequestSerializer(serializers.Serializer):
    elections = ElectionInputSerializer(many=True, min_length=2)

class VolatilityResultOutputSerializer(serializers.Serializer):
    from_election_id = serializers.CharField()
    to_election_id = serializers.CharField()
    from_year = serializers.IntegerField()
    to_year = serializers.IntegerField()
    volatility_index = serializers.FloatField()

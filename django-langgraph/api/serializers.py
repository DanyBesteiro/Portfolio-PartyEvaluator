from rest_framework import serializers

class PartySimilaritiesComparatorRequestSerializer(serializers.Serializer):
    candidature =  serializers.DictField()

    party_similarities = serializers.ListField(
        child=serializers.JSONField()
    )

class PartyValidatorRequestSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=6)
    name = serializers.CharField(max_length=250)
    acronym = serializers.CharField(max_length=25)
    formatted_acronym = serializers.CharField(max_length=26)
    provincial_head_code = serializers.CharField(max_length=6)
    autonomic_head_code = serializers.CharField(max_length=6)
    national_head_code = serializers.CharField(max_length=6)
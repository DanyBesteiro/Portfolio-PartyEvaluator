from rest_framework import serializers

class PartySimilaritiesComparatorRequestSerializer(serializers.Serializer):
    candidature =  serializers.DictField()

    similarities = serializers.ListField(
        child=serializers.JSONField()
    )

class SimilarityJoinerItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    acronym = serializers.CharField(max_length=50, required=True)
    nameSimilarity = serializers.FloatField()
    acronymSimilarity = serializers.FloatField()


class PartySimilaritiesJoinerRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, required=True)
    acronym = serializers.CharField(max_length=50, required=True)
    similarities = serializers.ListField(
        child=SimilarityJoinerItemSerializer()
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
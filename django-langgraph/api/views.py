from rest_framework.decorators import api_view
from .authentication import require_api_token
from .serializers import PartySimilaritiesComparatorRequestSerializer, PartyValidatorRequestSerializer
from .services.party_similarities_comparator.main import PartySimilaritiesComparatorService
from .services.party_validator.main import PartyValidatorService

@require_api_token
@api_view(["POST"])
def party_compare_similarities(request):
    serializer = PartySimilaritiesComparatorRequestSerializer(data=request.data, many = True)
    serializer.is_valid(raise_exception=True)
    
    service = PartySimilaritiesComparatorService()

    return service.compare(serializer.validated_data)

@require_api_token
@api_view(["POST"])
def party_validate(request):
    serializer = PartyValidatorRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    service = PartyValidatorService()

    return service.validate(candidature=serializer.validated_data)
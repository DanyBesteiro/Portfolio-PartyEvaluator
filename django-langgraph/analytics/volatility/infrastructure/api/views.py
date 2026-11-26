from rest_framework import status
from rest_framework.response import Response
#from rest_framework.views import APIView

from rest_framework.decorators import api_view
from config.authentication import require_api_token

from analytics.volatility.application.use_case import CalculatePedersenVolatilityUseCase
from ...domain.services import PedersenVolatilityCalculator
from .serializers import (
    VolatilityCalculationRequestSerializer,
    VolatilityResultOutputSerializer,
)

@require_api_token
@api_view(["POST"])
#class PedersenVolatilityView(request):
def pedersen_volatility_calculation(request):
    input_serializer = VolatilityCalculationRequestSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    use_case = CalculatePedersenVolatilityUseCase(
        calculator=PedersenVolatilityCalculator()
    )

    try:
        results = use_case.execute(input_serializer.validated_data["elections"])
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    output_serializer = VolatilityResultOutputSerializer(results, many=True)
    return Response({"volatility_series": output_serializer.data}, status=status.HTTP_200_OK)

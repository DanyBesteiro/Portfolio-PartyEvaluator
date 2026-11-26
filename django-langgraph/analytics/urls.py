from django.urls import path
from .volatility.infrastructure.api.views import pedersen_volatility_calculation

urlpatterns = [
    path("volatility/", pedersen_volatility_calculation, name="pedersen_volatility"), 
]
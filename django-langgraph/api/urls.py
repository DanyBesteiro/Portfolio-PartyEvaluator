from django.urls import path
from .views import party_compare_similarities, party_join_similarities, party_validate

urlpatterns = [
    path("party/comparator/", party_compare_similarities),
    path("party/joiner/", party_join_similarities),
    path("party/validate/", party_validate)
]
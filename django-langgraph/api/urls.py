from django.urls import path
from .views import party_compare_similarities, party_join_similarities, party_validate

urlpatterns = [
    path("comparator/", party_compare_similarities),
    path("joiner/", party_join_similarities),
    path("validate/", party_validate),
]
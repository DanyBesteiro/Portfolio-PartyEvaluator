from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def home(request):
    return JsonResponse({
        "service": "django-langgraph",
        "status": "ok"
    })

urlpatterns = [
    path("", home),
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
]

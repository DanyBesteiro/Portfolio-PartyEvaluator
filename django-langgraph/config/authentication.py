import secrets
from functools import wraps

from django.conf import settings
from django.http import JsonResponse


def require_api_token(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        expected_token = getattr(
            settings,
            "DJANGO_API_TOKEN",
            "",
        )

        authorization = request.headers.get(
            "Authorization", ""
        )

        scheme, _, provided_token = authorization.partition(" ")

        if (
            not expected_token
            or scheme.lower() != "bearer"
            or not provided_token
            or not secrets.compare_digest(
                provided_token,
                expected_token,
            )
        ):
            return JsonResponse(
                {"detail": "No autorizado"},
                status=401,
            )

        return view_func(request, *args, **kwargs)

    return wrapper
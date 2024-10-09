from django.conf import settings
from django.http import JsonResponse
from django.http.request import HttpRequest
from django.urls import reverse


def root(request: HttpRequest) -> JsonResponse:
    site_url = request.get_host()

    info = {
        "Name": "Django starterkit",
        "Site url": site_url,
        "Admin panel": site_url + "/admin",
        "API V1": {
            "swagger": site_url + reverse("swagger"),
            "redoc": site_url + reverse("redoc"),
        },
    }
    if settings.DEBUG:
        info["Profiler"] = site_url + "/silk"

    return JsonResponse(info)

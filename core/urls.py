"""
URL configuration for the project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .root_view import root

urlpatterns = [
    path("", root, name="root"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.api.v1.urls"), name="api-v1"),
]
if settings.DEBUG:
    static_urls = [
        urlpattern
        for urlpattern in (
            # the * start before static is used for sequence unpacking
            # because static returns a list of urlpatterns
            *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        )
    ]

    urlpatterns.extend(
        [
            *static_urls,
            path("silk/", include("silk.urls", namespace="silk"), name="silk"),
        ]
    )

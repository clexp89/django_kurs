"""
Projekt URLs
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings


urlpatterns = [
    path("", include("pages.urls")),
    path("api/token", obtain_auth_token, name="get_api_token"),  # via POST
    path("api/", include("events.api.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),
    path("artikelanlage/", include("artikelanlage.urls")),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

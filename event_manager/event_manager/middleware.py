"""
Projektweite Middleware-Klassen
"""

from django.utils import timezone
from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings


class AddDateMiddleware:
    """Füge das aktuelle Datum zum Kontext hinzu."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """Wird in den Kontext übergeben."""
        response.context_data["current_timestamp"] = timezone.now()
        return response


class RequireLoginMiddleware:
    """Middleware um Zugriff auf eine App zu gewährleisten."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # VOR der MIDDLEWARE was machen
        response = self.get_response(request)
        # NACH der MIDDLEWARE machen
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Check if app is proteced."""
        protected_apps = settings.PROTECTED_APPS  # besser in settings oder .env

        # docs: Returns the path, plus an appended query string, if applicable.
        path = request.get_full_path()

        if resolve(request.path_info).app_name in protected_apps:
            if not request.user.is_authenticated:
                return redirect(f"{settings.LOGIN_URL}?next={path}")

        return None

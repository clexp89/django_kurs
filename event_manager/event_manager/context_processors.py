""" 
Context Process:
ist eine Funktion, die es ermöglicht, einen zustätzlichen
Kontext in die Template-Engine zu übertragen.
"""

from django.contrib.sites.models import Site


def get_site_name(request):
    current_site_name = Site.objects.get_current().name

    return {"get_site_name_site_name": current_site_name}

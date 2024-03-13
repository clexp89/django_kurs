from django.shortcuts import render
from django.views.generic import TemplateView
from events.models import Event, Category


class HomePageView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs) -> dict:
        ctx = super().get_context_data(**kwargs)
        ctx["events"] = Event.objects.all()[:10]
        ctx["categories"] = Category.objects.all()[:5]
        return ctx

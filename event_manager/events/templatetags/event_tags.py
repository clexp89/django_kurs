""" 
eigenen Filter anlegen.

Filter hier definieren und später im Template importieren (load)
{% load event_tags %}

z.b.
<h1>{{event.name|my_filter}}</h1>
"""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def safe_query_string(context, **kwargs) -> str:
    """
    erzeuge einen URL-encoded String aus den Get-Parametern
    page=1&q=suchwort
    """
    query = context["request"].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def is_group_member(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def my_filter(value):
    return value[1:-1].lower()

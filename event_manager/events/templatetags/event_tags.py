""" 
eigenen Filter anlegen.

Filter hier definieren und später im Template importieren (load)
{% load event_tags %}

z.b.
<h1>{{event.name|my_filter}}</h1>
"""

from django import template

register = template.Library()


@register.filter
def is_group_member(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def my_filter(value):
    return value[1:-1].lower()

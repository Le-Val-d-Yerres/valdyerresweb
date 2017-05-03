from django import template
from menu.views import TopMenu
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def getmenu():
    return mark_safe(TopMenu())
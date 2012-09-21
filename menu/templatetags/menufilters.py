from django import template
from menu.views import TopMenu

register = template.Library()

@register.tag(name="getmenu")
def getmenu():
    return "meuh"
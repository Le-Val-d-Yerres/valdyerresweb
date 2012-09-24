from django import template
from menu.views import TopMenu

register = template.Library()

@register.simple_tag()
def getmenu():
    return TopMenu()
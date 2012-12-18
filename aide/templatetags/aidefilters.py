# -*- coding: utf-8 -*-

from django import template
from aide.models import Aide
from aide.views import renderModal

register = template.Library()
cache={}
@register.filter(is_safe=True)
def aide(aideslug):
    try:
        aide = cache[aideslug]
    except:
        aide = Aide.objects.get(slug = aideslug)
        cache[aideslug] = aide
    return renderModal(aide)
    
    
    
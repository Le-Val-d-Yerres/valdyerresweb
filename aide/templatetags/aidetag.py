from django import template
from aide.models import Aide
from aide.views import renderModal

register = template.Library()

@register.filter(is_safe=True)
def aide(aideslug):
    aide = Aide.objects.get(slug = aideslug)
    return renderModal(aide)
    
    
    
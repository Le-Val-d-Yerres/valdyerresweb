# -*- coding: utf-8 -*-

from django import template
from evenements.lib.eventAddLink import getLinkList, getEventsLinkList, getSaisonLinkList
register = template.Library()

@register.filter(is_safe=True)
def calendaraddlinklist(evenement):
    text = u"<ul style=\"list-style:none;\" >\n"
    for line in getLinkList(evenement):
        text += u"<li>"+line+"</li>\n"
    text += u"</ul>\n"
    return text
        
@register.filter(is_safe=True)
def calendarexportlinklist(dictargs):
    text = u"<ul style=\"list-style:none;\" >\n"
    for line in getEventsLinkList(dictargs):
        text += u"<li>"+line+"</li>\n"
    text += u"</ul>\n"
    return text

@register.filter(is_safe=True)
def saisonexportlinklist(saisonslug):
    text = u"<ul style=\"list-style:none;\" >\n"
    for line in getSaisonLinkList(saisonslug):
        text += u"<li>"+line+"</li>\n"
    text += u"</ul>\n"
    return text
        

    

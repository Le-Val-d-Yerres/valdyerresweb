# -*- coding: utf-8 -*-

from django import template
from evenements.lib.eventAddLink import getLinkList, getEventsLinkList, getSaisonLinkList
register = template.Library()
import datetime
from datetime import timedelta

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
        
@register.filter(is_safe=True)
def duree(debut,fin):
    delta = fin - debut
    txttemps = ""
    jours = delta.seconds/(3600*24)
    secondes = delta.seconds - (jours * 3600 * 24)
    heures = secondes/3600
    secondes = secondes - (heures*3600)
    minutes = secondes/60
    if jours > 0:
        txttemps = str(delta.days)
        if jours == 1:
            txttemps += "jour"
        if jours > 1:
            txttemps += "jours"
    if heures > 0 :
        txttemps+=" "+str(heures)+"H"
    if minutes > 0 :    
        txttemps+= " "+str(minutes)+"min"
    return txttemps
    
    

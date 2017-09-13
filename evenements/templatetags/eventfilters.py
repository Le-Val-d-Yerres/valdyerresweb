# -*- coding: utf-8 -*-

from django import template
from evenements.lib.eventAddLink import getLinkList, getEventsLinkList, getSaisonLinkList
register = template.Library()
import datetime
from datetime import timedelta

@register.filter(is_safe=True)
def calendaraddlinklist(evenement):
    text =""
    for line in getLinkList(evenement):
        text += u"<dl class=\"linklist\" >\n"
        text += line+"\n"
        text += u"</dl>\n"
    return text
        
@register.filter(is_safe=True)
def calendarexportlinklist(dictargs):
    text = ""
    for line in getEventsLinkList(dictargs):
        text += u"<dl class=\"linklist\" >\n"
        text += line+"\n"
        text += u"</dl>\n"
    return text

@register.filter(is_safe=True)
def saisonexportlinklist(saisonslug):
    text = ""
    for line in getSaisonLinkList(saisonslug):
        text += u"<dl class=\"linklist\" >\n"
        text += line+"\n"
        text += u"</dl>\n"
    return text
        
@register.filter(is_safe=True)
def duree(debut,fin):
    delta = fin - debut
    txttemps = ""
    secondes = delta.seconds - (delta.days * 3600 * 24)

    heures = int(secondes/3600)
    secondes = secondes - (heures*3600)

    minutes = int(secondes/60)
    if delta.days > 0:
        txttemps = str(delta.days)
        if delta.days == 1:
            txttemps += " jour"
        if delta.days > 1:
            txttemps += " jours"
    if heures > 0:
        txttemps += " "+str(heures)+" h"
    if minutes > 0:
        if len(str(minutes)) < 2:
            minutes = "0"+str(minutes)
        txttemps += " "+str(minutes)+" min"
    return txttemps


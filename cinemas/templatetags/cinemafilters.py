# -*- coding: utf-8 -*-

from django import template
from evenements.lib.eventAddLink import getLinkList, getEventsLinkList, getSaisonLinkList
register = template.Library()



@register.filter(is_safe=True)
def dureesec(secondes):
    txttemps = ""
    jours = secondes/(3600*24)
    secondes = secondes - (jours * 3600 * 24)
    heures = secondes/3600
    secondes = secondes - (heures*3600)
    minutes = secondes/60
    if jours > 0:
        txttemps = str(jours)
        if jours == 1:
            txttemps += "jour"
        if jours > 1:
            txttemps += "jours"
    if heures > 0 :
        txttemps+=" "+str(heures)+"H"
    if minutes > 0 :    
        txttemps+= " "+str(minutes)+"min"
    return txttemps
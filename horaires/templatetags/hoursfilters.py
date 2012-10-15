# -*- coding: utf-8 -*-

from django import template
from horaires.models import Periode,Horaires,Jour
register = template.Library()
import datetime


def horaires_journee(day,horaires):
    myday = horaires.GetDay(day.isoweekday())
    if myday.journee_continue:
        return myday.jourNom+u", journée continue de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")
    
    if myday.journee_continue:
        return myday.jourNom+u": journée continue"
    
    txthours = myday.jourNom+" : "
    if myday.matin_ferme:
        txthours += u"fermé la matinée"
    else:
        txthours += u"matin de :"+myday.heure_matin_debut.strftime("%H:%M")+"à"+myday.heure_matin_fin.strftime("%H:%M")
    if myday.am_ferme:
        txthours += u"fermé l'après-midi"
    else:
        txthours += u"après-midi de :"+myday.heure_matin_debut.strftime("%H:%M")+"à"+myday.heure_matin_fin.strftime("%H:%M")
    
    if myday.matin_ferme and myday.am_ferme:
        return myday.jourNom+u": fermé toute la journée"
    
   
    
    return txthours


@register.filter(is_safe=True)
def horaires_aujourdhui(horaires):
    today = datetime.datetime.today()
    return horaires_journee(today,horaires)













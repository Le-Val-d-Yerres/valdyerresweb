# -*- coding: utf-8 -*-

from django import template
register = template.Library()
import datetime

WeekDay = ['lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi','dimanche']    


def horaires_journee(day,horaires):
    txthours = ""
    myday = horaires.GetDay(day.isoweekday())
    if myday.matin_ferme and myday.am_ferme:
        return myday.jourNom+": fermé toute la journée"
    
    if myday.journee_continue:
        return "journée continue de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")+"."
    
    if myday.matin_ferme:
        txthours += "fermé la matinée, "
    else:
        txthours += "matin de :"+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_matin_fin.strftime("%H:%M")+", "
    if myday.am_ferme:
        txthours += "fermé l'après-midi"
    else:
        txthours += "après-midi de :"+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_matin_fin.strftime("%H:%M")
    
    
    
    return txthours+"." 


@register.filter(is_safe=True)
def horaires_aujourdhui(horaires):
    today = datetime.datetime.today()
    return horaires_journee(today,horaires)

@register.filter(is_safe=True)
def horaires_demain(horaires):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return horaires_journee(tomorrow,horaires)

@register.simple_tag()
def nom_jour_aujourdhui():
    today = datetime.datetime.today()
    
    return WeekDay[today.weekday()]


@register.simple_tag()
def nom_jour_demain():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return WeekDay[tomorrow.weekday()]









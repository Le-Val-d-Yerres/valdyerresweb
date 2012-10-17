# -*- coding: utf-8 -*-

from django import template
register = template.Library()
import datetime

mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
WeekDay = ['lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi','dimanche']    

#une journée en général 
def horaires_journee(numjour,horaires):
    txthours = ""
    myday = horaires.GetDay(numjour)
    if myday.matin_ferme and myday.am_ferme:
        return myday.jourNom+": fermé toute la journée"
    
    if myday.journee_continue:
        return "journée continue de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")+"."
    
    if myday.matin_ferme:
        txthours += "fermé la matinée, "
    else:
        txthours += "matin de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_matin_fin.strftime("%H:%M")+", "
    if myday.am_ferme:
        txthours += "fermé l'après-midi"
    else:
        txthours += "après-midi de "+myday.heure_am_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")
    return txthours+"."

#un jour précis
def horaires_jour(day,horaires):
    return horaires_journee(day.isoweekday(), horaires)  

@register.filter(is_safe=True)
def horaires_semaine(horaires):
    txthoraires = ""
    for day in range(1,8):
        txthoraires += "<li>"+WeekDay[day-1].capitalize()+" : "+horaires_journee(day, horaires)+"</li>"
    return txthoraires

@register.filter(is_safe=True)
def horaires_aujourdhui(horaires):
    today = datetime.datetime.today()
    return horaires_jour(today,horaires)

@register.filter(is_safe=True)
def horaires_demain(horaires):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return horaires_jour(tomorrow,horaires)

@register.simple_tag()
def nom_jour_aujourdhui():
    today = datetime.datetime.today()
    
    return WeekDay[today.weekday()]


@register.simple_tag()
def nom_jour_demain():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return WeekDay[tomorrow.weekday()]

@register.filter(is_safe=True)
def dates_periode(debut, fin):
    text = u"du "+WeekDay[int(debut.strftime("%w"))]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+" "+debut.strftime(u"%Y") + " au "+WeekDay[int(fin.strftime(u"%w"))]+u" "+fin.strftime(u"%d")+u" "+mois[int(fin.strftime(u"%m"))-1]+" "+fin.strftime(u"%Y")
    return text







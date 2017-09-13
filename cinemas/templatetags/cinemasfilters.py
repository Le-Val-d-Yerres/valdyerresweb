# -*- coding: utf-8 -*-

from django import template
from cinemas.lib.eventAddlink import getLinkList
from pytz import timezone
from django.conf import settings
import datetime
register = template.Library()

jours = ['lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi',u'dimanche',]
mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
mois_courts = [u'jan', u'fév', u'mars', u'avril', u'mai', u'juin', u'juil', u'août', u'sept', u'oct', u'nov' ,u'déc']

@register.filter(is_safe=True)
def dureesec(secondes):
    txttemps = ""
    jours = int(secondes/(3600*24))
    secondes = int(secondes - (jours * 3600 * 24))
    heures = int(secondes/3600)
    secondes = int(secondes - (heures*3600))
    minutes = int(secondes/60)
    if jours > 0:
        txttemps = str(jours)
        if jours == 1:
            txttemps += "jour"
        if jours > 1:
            txttemps += "jours"
    if heures > 0 :
        txttemps+=str(heures)+"h"
    if minutes > 0 :
        if len(str(minutes)) < 2:
            minutes = "0"+str(minutes)
        txttemps+=str(minutes)+"min"
    return txttemps

@register.filter(is_safe=True)
def queljour(thedate):  
    TZone = timezone(settings.TIME_ZONE)
    now = datetime.datetime.now(TZone)
    deltanow = thedate-now.date()
    if deltanow.days == 0:
        text = u"<strong>Aujourd'hui</strong>"
    elif deltanow.days == 1:
        text = u"Demain"
    else :
        text = jours[thedate.weekday()]+u" "+thedate.strftime(u"%d")+u" "+mois[int(thedate.strftime(u"%m"))-1]
        text = text.capitalize()
    return text

@register.filter(is_safe=True)
def quelleheure(thedate):   
    TZone = timezone(settings.TIME_ZONE)
    thedate = thedate.astimezone(TZone)
    return thedate.strftime(u"%H:%M")

@register.filter(is_safe=True)
def seanceaddlinklist(seance):
    text = u"<ul style=\"list-style:none;\" >\n"
    for line in getLinkList(seance):
        text += u"<li style=\"margin-top:5px;\">"+line+"</li>\n"
    text += u"</ul>\n"
    return text
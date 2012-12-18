# -*- coding: utf-8 -*-

from django import template
from cinemas.lib.eventAddlink import getLinkList
from pytz import timezone
from django.conf import settings
import datetime
register = template.Library()

jours = [u'dimanche',u'lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi']
mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
mois_courts = [u'jan', u'fév', u'mars', u'avril', u'mai', u'juin', u'juil', u'août', u'sept', u'oct', u'nov' ,u'déc']

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
        txttemps+=str(heures)+"H"
    if minutes > 0 :    
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
        text = u"demain"
    else :    
        text = jours[int(thedate.strftime(u"%w"))]+u" "+thedate.strftime(u"%d")+u" "+mois[int(thedate.strftime(u"%m"))-1]
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
        text += u"<li>"+line+"</li>\n"
    text += u"</ul>\n"
    return text
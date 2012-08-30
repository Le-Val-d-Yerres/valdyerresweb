# -*- coding: utf-8 -*-
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from evenements.views import *
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from pytz import timezone
import pytz
from django.conf import settings
from django.core.urlresolvers import reverse

def entierAvecZero(entier):
    if entier < 10:
        result = "0"+str(entier)
    else:
        result = str(entier)
    return result

class CAVYCalendar(HTMLCalendar):
    
    listeJour = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    listeMois = ['Janvier', u'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', u'Août', 'Septembre', 'Octobre', 'Novembre', u'Décembre']
    
    def __init__(self, evenements, firstweekday=0):
        self.ListeEvenement = evenements
        self.evenementIterateur = 0
        self.firstweekday = firstweekday
        
    def formatweekday(self, day):
        s = self.listeJour[day]
        return '<th class="%s">%s</th>' % (self.cssclasses[day], s)
    
    def formatmonthname(self, theyear, themonth, withyear = True):
        month = entierAvecZero(themonth)
        content = "<a href="+reverse('agenda-mois', kwargs={'annee': theyear, 'mois': month})+">"+self.listeMois[themonth-1]+"</a> "
        content = content+"<a href="+reverse('agenda-annee', kwargs={'annee': theyear})+">"+str(theyear)+"</a>"
        return '<tr><th colspan="7" class="month">'+content+'</th></tr>'
            
    def formatday(self, day, weekday):
        if day != 0:
            
            content = str(day)+"<br \>"
            TZone = timezone('UTC')

            for each in self.ListeEvenement:
                dateDebut = each.debut.astimezone(TZone)
                dateFin = each.fin.astimezone(TZone)

                if int(dateDebut.strftime("%d")) <= day and day <= int(dateFin.strftime("%d")):
                    
                    content = content+"<p><a href="+reverse('event-details', kwargs={'slug': each.cadre_evenement.slug, 'evenement_slug': each.slug })+">"+each.nom+"</a><br \>"
                    content = content+each.type.nom+"<br \>"
                    if dateDebut.strftime("%d") == dateFin.strftime("%d"):
                        content = content+"De "+dateDebut.strftime("%H")+"h"+dateDebut.strftime("%M")+u" à "+dateFin.strftime("%H")+"h"+dateFin.strftime("%M")
                    else:
                        if dateDebut.strftime("%d") == day:
                            content = content+"A partir de "+dateDebut.strftime("%H")+"h"+dateDebut.strftime("%M")
                        elif dateFin.strftime("%d") == day:
                            content = content+"Jusqu'à "+dateFin.strftime("%H")+"h"+dateFin.strftime("%M")
                        else:
                            content = content+"Toute la journée"
                        content = content+"</p>"
                    self.ListeEvenement.remove(each)
                else:
                    break
            return '<td class="dayNumber">'+content+'</td>'
        else:
            return '<td class="noday">&nbsp;</td>' # day outside month

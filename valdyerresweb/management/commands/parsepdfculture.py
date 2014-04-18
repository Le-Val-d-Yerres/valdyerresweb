# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from datetime import datetime, date, time, timedelta
from django.template import defaultfilters
import os
from evenements.models import Evenement, Organisateur, TypeEvenement
from pytz import timezone
from valdyerresweb import settings
from localisations.models import Lieu

myTimezone = timezone(settings.TIME_ZONE)


mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
jours = [u'dimanche',u'lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi']
types = [u'MUSIQUE CLASSIQUE', u'HUMOUR',u'DANSE', u'CHANSON',u'THÉÂTRE',u'COMÉDIE MUSICALE', u'SPECTACLE MUSICAL',
         u'CONTE MUSICAL', u'GRAND SPECTACLE', u'GRAND SPECTACLE / CABARET',u'THÉÂTRE / HUMOUR',u"THÉÂTRE CLASSIQUE"]
id_salles_spectacles = {u'BOUSSY-SAINT-ANTOINE': 5, u'YERRES': 6, u'BRUNOY': 8, u'CROSNE': 9, u'ÉPINAY-SOUS-SÉNART': 24,u'QUINCY-SOUS-SÉNART': 10}

eventlist = list()

class evenement(object):

    def __init__(self):
        self.nom = ""
        self.description = ""
        self.debut = ""
        self.fin = ""
        self.image = ""
        self.type = ""
        self.lieu = ""
        self.copyrightimg=""



def proceed(filename):
    f = open(filename)
    event = evenement()
    for line in f.readlines():
        line = unicode(line, encoding="utf-8")
        if u"©" in line:
            event.copyrightimg = line.strip()

        if line.strip() == u"" or u"©" in line :
            continue
        words = line.split(" ")
        charlower = u"".join([c for c in line if c.islower()])

        if words[0].isupper() or words[0] is u"«" or words[0] is u"&" :
             if words[0].lower() not in jours and line.strip() not in types:
                if u"€" not in line and u"/" not in line and event.description is "" :
                    event.nom = event.nom+u" " + line
                    event.nom = event.nom.strip().title()
        if len(words) > 1 and charlower.islower():
            event.description = event.description+" " + line
            event.description = event.description.strip()
        if event.description is not "" and u"€" not in line and words[0].lower() not in jours:
            if words[0].isupper() and line.strip() not in types:
                event.description = event.description+"\n" + line.title()
                event.description = event.description.strip()

        if line.strip() in types:
            line = line.split(u"/")[0]
            event.type = line.strip().capitalize()

        if words[0].lower() in jours:
            jour, lieu = line.split(u"/")
            event.lieu = lieu.strip()
            numjour = words[1]
            nummois = 99
            if numjour == u"1ER":
                numjour = 1
            numjour = int(numjour)
            for i, m in enumerate(mois):
                if words[2].lower() in m :

                    nummois = int(i)+1
                    break
            numannee = 0
            if nummois > 6:
                numannee = 2014
            else:
                numannee = 2015
            mydate = date(numannee, nummois,numjour)
            heure, minutes = words[4].split(u'H')
            heure = int(heure)
            if minutes == "":
                minutes = 0
            else:
                minutes = int(minutes)
            mytime = time(heure, minutes)
            event.debut = datetime.combine(mydate, mytime)





        if u"[" in line and u"]" in line :

            heures, minutes = words[3].split(u"H")
            if minutes == u"":
                minutes = 0
            else:
                minutes = int(minutes)
            heures = int(heures)
            delta = timedelta(hours=heures, minutes=minutes)

            event.fin = event.debut + delta
            # print(u"-------------------------------------------")
            # print(event.nom)
            # print(event.description)
            # print(event.debut)
            # print(event.fin)
            # print(event.type)
            # print(event.lieu)
            # print(event.copyrightimg)
            eventlist.append(event)
            event = evenement()


def imgtraitement():
    mypath = os.path.abspath(os.path.split(__file__)[0])
    imgpath = os.path.join(mypath,"img-test")
    for i, event in enumerate(eventlist):
        img = os.path.join( imgpath, str(i)+".jpg")
        imgname = os.path.join(imgpath,defaultfilters.slugify(event.nom)+".jpg")
        command = u"convert "+img+u" -fill white -gravity southeast -annotate 0 '"+event.copyrightimg+u"' "+imgname
        #shlex ne supporte pas le caractère copyright et il a bien raison
        #du coup on récupère les commandes et on les lance dans le terminal
        print(command)
    return 1

def corresp():
    imgpath = "uploads/evenements/"
    orga = Organisateur.objects.get(id=2)
    for i, event in enumerate(eventlist):
        evenement = Evenement()

        evenement.slug = defaultfilters.slugify(event.nom)
        listevenement = Evenement.objects.filter(slug__startswith=evenement.slug)
        listsize = len(listevenement)

        if listsize > 0:
            evenement.slug = evenement.slug+'-'+str(listsize+1)

        type = TypeEvenement.objects.get(slug=defaultfilters.slugify(event.type))
        evenement.nom = event.nom
        evenement.description = event.description
        evenement.debut = myTimezone.localize(event.debut)
        evenement.fin = myTimezone.localize(event.fin)
        evenement.cadre_evenement_id = 10
        evenement.lieu_id = id_salles_spectacles[event.lieu]
        evenement.meta_description = evenement.nom + evenement.description[0:75]
        evenement.image = os.path.join(imgpath,defaultfilters.slugify(event.nom)+".jpg")
        evenement.type = type
        evenement.publish = True
        evenement.save()
        evenement.organisateur.add(orga)
        evenement.save()




class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        mypath = os.path.abspath(os.path.split(__file__)[0])
        proceed(os.path.join(mypath,'Saison_Culturelle_du_Val_d_Yerres_Abonnements_2014_2015.txt'))
        #imgtraitement()
        corresp()

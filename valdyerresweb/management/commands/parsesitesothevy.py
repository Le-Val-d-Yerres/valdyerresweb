# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import subprocess
import shlex

from django.core.management.base import NoArgsCommand
from datetime import datetime, date, time, timedelta
from django.template import defaultfilters
import os
from evenements.models import Evenement, Organisateur, TypeEvenement
from pytz import timezone
from valdyerresweb import settings
from localisations.models import Lieu
import codecs


mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
jours = [u'dimanche',u'lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi']
types = [u'MUSIQUE CLASSIQUE', u'HUMOUR',u'DANSE', u'CHANSON',u'THÉÂTRE',u'COMÉDIE MUSICALE', u'SPECTACLE MUSICAL',
         u'CONTE MUSICAL', u'GRAND SPECTACLE', u'GRAND SPECTACLE / CABARET',u'THÉÂTRE / HUMOUR',u"THÉÂTRE CLASSIQUE"]
id_salles_spectacles = {u'BOUSSY-SAINT-ANTOINE': 5, u'YERRES': 6, u'BRUNOY': 8, u'CROSNE': 9, u'EPINAY-SOUS-SENART': 24, u'QUINCY-SOUS-SENART': 10}

liste_themes = {
    u'Chanson': u'http://spectacles.levaldyerres.fr/fr/spectacles/recital.html',
    u'Humour': u'http://spectacles.levaldyerres.fr/fr/spectacles/copy_opera.html',
    u'Théâtre': u'http://spectacles.levaldyerres.fr/fr/spectacles/copy_theatre.html',
    u'Danse': u'http://spectacles.levaldyerres.fr/fr/spectacles/copy_danse.html',
    u'Musique': u'http://spectacles.levaldyerres.fr/fr/spectacles/copy_musique.html',

}


class evenement(object):

    def __init__(self):
        self.nom = ""
        self.description = ""
        self.debut = ""
        self.fin = ""
        self.image = ""
        self.type = ""
        self.lieu = ""
        self.copyrightimg = ""


def parse_page(url):
    evt = evenement()
    r = requests.get(url)
    data_html = r.text
    soup = BeautifulSoup(data_html)

    nom = soup.find("h1").string
    nom = unicode(nom)

    dateheureville = soup.find("div", {"class": "about-project bottom-2"}).next
    dateevt, heure = dateheureville.split("|")
    dateevt = dateevt.strip()
    dateevt = dateevt.split(" ")

    if dateevt[1].lower() == u"1er":
        numjour = 1
    else:
        numjour = int(dateevt[1])
    nummois = 99
    for i, m in enumerate(mois):
        if dateevt[2].lower() in m:
            nummois = int(i)+1
            break

    numannee = 2016
    if nummois > 6:
        numannee = 2015

    dateevt = date(numannee, nummois, numjour)


    heure = heure.strip()
    heure, minutes = heure.split("h")
    heure = int(heure)

    if minutes == "":
        minutes = 0
    else:
        minutes = int(minutes)

    heure_debut = time(heure, minutes)

    dateevt = datetime.combine(dateevt, heure_debut)

    ville = dateheureville.next.next
    ville = ville.strip()

    duree = soup.find("ul", {"class": "arrow-list job bottom-2"})
    duree = duree.findAll("li")

    try:
        duree = duree[1].text.split(":")[1].strip()
    except:
        duree = "1h30"
    duree_heure, duree_minute = duree.split("h")
    duree_heure = int(duree_heure)
    if duree_minute == "":
        duree_minute = 0
    else:
        duree_minute = int(duree_minute)

    duree = time(duree_heure,duree_minute)

    heure_fin = dateevt + timedelta(hours=duree_heure, minutes=duree_minute)

    urlimage = soup.find("div", {"class": "twelve columns top-1 bottom-3"}).find("img")["src"]
    urlimage = "http://spectacles.levaldyerres.fr/"+urlimage

    bloc = soup.findAll("div", {"class": "twelve columns top-1 bottom-3"})[1]

    tabtxt = bloc.get_text().strip().split("\n")


    tabtxtclean = [txt for txt in tabtxt if txt.strip() is not u""]

    desc = str()
    for txt in tabtxtclean[3:]:
        desc = desc + txt+u"<br>"

    if soup.find("iframe") is not None:
        desc += str(soup.find("iframe"))

    desc = desc.encode("utf-8")
    desc = desc.replace("ᵉ","ème")
    desc = desc.replace(codecs.BOM_UTF8,"")

    evt.nom = nom.encode("utf-8").strip()
    evt.debut = dateevt
    evt.fin = heure_fin
    if u"CEC" in ville:
        ville = u"YERRES"
    evt.lieu = ville
    evt.description = desc
    evt.image = urlimage

    return evt


def parse_list(url):
    link_list = list()
    r = requests.get(url)
    data_html = r.text
    soup = BeautifulSoup(data_html)
    list_evt = soup.findAll("div", {"class": "category"})

    for item in list_evt:
        link = item.find("a")["href"]
        link = "http://spectacles.levaldyerres.fr"+link
        link_list.append(link)

    return link_list


def img_traitement(url, slug):
    img = requests.get(url)
    imgpath = "uploads/evenements/"
    imgpath = os.path.join(settings.MEDIA_ROOT, imgpath)
    imagetemppath = os.path.join(imgpath, "temp.jpg")
    imagepath = os.path.join(imgpath, slug+".jpg")
    with open(imagetemppath, 'wb') as test:
        test.write(img.content)
    command = u"convert "+imagetemppath+""+u" -resize 670x375 -background black -compose Copy -gravity center -extent 670x375 -quality 90 "+imagepath
    cmd = shlex.split(command)
    subprocess.call(cmd)


def corresp(eventlist):
    myTimezone = timezone(settings.TIME_ZONE)

    orga = Organisateur.objects.get(id=2)
    for event in eventlist:
        evenement = Evenement()
        imgpath = "uploads/evenements/"
        fullimagepath = os.path.join(settings.MEDIA_ROOT, imgpath)

        evenement.slug = defaultfilters.slugify(event.nom)



        listevenement = Evenement.objects.filter(slug__startswith=evenement.slug)
        listsize = len(listevenement)

        if listsize > 0:
            evenement.slug = evenement.slug+'-'+str(listsize+1)
        img_traitement(event.image, evenement.slug)

        type = TypeEvenement.objects.get(slug=defaultfilters.slugify(event.type))
        evenement.nom = event.nom
        print evenement.nom
        evenement.description = event.description

        evenement.debut = myTimezone.localize(event.debut)
        evenement.fin = myTimezone.localize(event.fin)
        evenement.cadre_evenement_id = 14
        evenement.lieu_id = id_salles_spectacles[event.lieu]
        meta_description = evenement.nom.decode('utf-8') +u" "+ evenement.description.decode("utf-8")
        meta_description = meta_description.replace("<br>",'')
        meta_description = meta_description[0:198]
        meta_description = meta_description.encode("utf-8")



        evenement.meta_description = meta_description
        evenement.image = os.path.join(imgpath, evenement.slug +".jpg")
        evenement.type = type
        evenement.publish = True
        evenement.save()
        evenement.organisateur.add(orga)
        evenement.save()


def proceed():
    liste_evenements = list()
    for type, url in liste_themes.iteritems():
        for link in parse_list(url):
            event = parse_page(link)
            event.type = type
            liste_evenements.append(event)
    return liste_evenements




class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        liste_evenements = list()
        liste_evenements = proceed()
        corresp(liste_evenements)
        #parse_page("http://spectacles.levaldyerres.fr/fr/robin-des-bois...-la-legende-ou-presque.html?cmp_id=77&news_id=424&vID=80")


#<iframe width="560" height="315" src="https://www.youtube.com/embed/ZnuwB35GYMY" frameborder="0" allowfullscreen></iframe>
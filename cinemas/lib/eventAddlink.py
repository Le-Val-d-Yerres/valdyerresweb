# -*- coding: utf-8 -*-

from cinemas.models import Seance
from django.core.urlresolvers import reverse
from pytz import timezone
from django.conf import settings
from valdyerresweb.templatetags.filtres import resume
import valdyerresweb.templatetags.filtres as filtres
from StringIO import StringIO
from django.http import HttpResponse
from django.template import Context,loader
from django.templatetags.static import static




class EventLink(object):
    text =u" Ajouter à votre agenda"
    
    def getLink(self,seance):
        raise NotImplementedError('Exception : EventLink is supposed to be an interface')
    def setLink(self,imgurl,linkurl):
        return "<a href=\""+linkurl+"\"><img src=\""+imgurl+"\">"+self.text+"</a>"
    
        
class OutlookEventLink(EventLink):
    def getLink(self,seance):
        self.text += u" Outlook"
        linkurl = reverse('seanceics', kwargs={'seance_id': seance.id})
        imgurl = static("valdyerresweb/img/evenements/40x40/outlook-icon-40x40.png")
        return self.setLink(imgurl,linkurl)
    
class GoogleEventLink(EventLink):
    def getLink(self, seance):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = seance.date_debut
        datefin = seance.date_fin
        self.text +=" Google"
        linkurl = u"http://www.google.com/calendar/event?"
        linkurl += u"&action=TEMPLATE"
        linkurl += u"&text="+seance.film.titre
        linkurl += u"&dates="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        if datefin != datedebut:
            linkurl += u"/"+datefin.strftime("%Y")+datefin.strftime("%m")+datefin.strftime("%d")+u"T"+datefin.strftime("%H")+datefin.strftime("%M")+u"00Z"
        linkurl += u"&sprop=website:"+settings.NOM_DOMAINE+reverse('seances')
        linkurl += u"&sprop=name:"+settings.NOM_ORGANISATION
        linkurl += u"&location="+seance.cinema.nom+u","+seance.cinema.rue+u","+seance.cinema.ville.nom
        linkurl += u"&details=Projection du film : "+seance.film.titre
        imgurl = static("valdyerresweb/img/evenements/40x40/gmail-icon-40x40.png")
        
        return self.setLink(imgurl,linkurl)
        
class YahooEventLink(EventLink):
    def getLink(self, seance):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = seance.date_debut
        datefin = seance.date_fin
        duree = datefin - datedebut
        
        self.text +=" Yahoo"
        linkurl = u"http://calendar.yahoo.com/?v=60"
        linkurl += u"&TITLE="+seance.film.titre
        linkurl += u"&ST="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        linkurl += u"&URL:"+settings.NOM_DOMAINE+reverse('seances')
        linkurl += u"&in_loc="+seance.cinema.nom+u","+seance.cinema.rue+u","+seance.cinema.ville.nom
        linkurl += u"&DESC=Projection du film : "+seance.film.titre
        imgurl = static("valdyerresweb/img/evenements/40x40/yahoo-icon-40x40.png")
        
        return self.setLink(imgurl,linkurl)

class IcalEventLink(EventLink):
    def getLink(self,seance):
        self.text += u" Ical"
        linkurl = reverse('seanceics', kwargs={'seance_id': seance.id})
        imgurl = static("valdyerresweb/img/evenements/40x40/ical-icon-40x40.png")
        return self.setLink(imgurl,linkurl)


def getLinkList(seance):
    eventAddLinkList = list()
    
    myOutlookEventLink = OutlookEventLink()
    myGoogleEventLink = GoogleEventLink()
    myYahooEventLink = YahooEventLink()
    myIcalEventLink = IcalEventLink()
    eventAddLinkList.append(myGoogleEventLink.getLink(seance))
    eventAddLinkList.append(myYahooEventLink.getLink(seance))
    eventAddLinkList.append(myOutlookEventLink.getLink(seance))
    eventAddLinkList.append(myIcalEventLink.getLink(seance))
    return eventAddLinkList
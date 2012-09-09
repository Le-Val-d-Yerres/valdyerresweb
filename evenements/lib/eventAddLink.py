# -*- coding: utf-8 -*-
from evenements.models import Evenement
from django.core.urlresolvers import reverse
from pytz import timezone
from django.conf import settings
from valdyerresweb.templatetags.filtres import resume

class EventLink(object):
    text =u" Ajouter à votre agenda"
    
    def getLink(self,evenement):
        raise NotImplementedError('Exception : EventAdder is supposed to be an interface')
    def setLink(self,imgurl,linkurl):
        return "<a href=\""+linkurl+"\"><img src=\""+imgurl+"\">"+self.text+"</a>"

        
class OutlookEventLink(EventLink):
    def getLink(self,evenement):
        self.text += u" Outlook"
        linkurl = reverse('event-details-ics', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl = "/static/img/evenements/40x40/outlook-icon-40x40.png"
        return self.setLink(imgurl,linkurl)
    
class GoogleEventLink(EventLink):
    def getLink(self, evenement):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = evenement.debut
        datefin = evenement.fin
        self.text +=" Google"
        linkurl = u"http://www.google.com/calendar/event?"
        linkurl += u"&action=TEMPLATE"
        linkurl += u"&text="+evenement.nom
        linkurl += u"&dates="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        if datefin != datedebut:
            linkurl += u"/"+datefin.strftime("%Y")+datefin.strftime("%m")+datefin.strftime("%d")+u"T"+datefin.strftime("%H")+datefin.strftime("%M")+u"00Z"
        linkurl += u"&sprop=website:"+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        linkurl += u"&sprop=name:"+settings.NOM_ORGANISATION
        linkurl += u"&location="+evenement.lieu.nom_lieu+u","+evenement.lieu.rue+u","+evenement.lieu.ville.nom
        linkurl += u"&details="+evenement.type.nom+" : "+resume(evenement.description, 150) +" "+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl =  "/static/img/evenements/40x40/gmail-icon-40x40.png"
        return self.setLink(imgurl,linkurl)
        
class YahooEventLink(EventLink):
    def getLink(self, evenement):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = evenement.debut
        datefin = evenement.fin
        duree = datefin - datedebut
        
        self.text +=" Yahoo"
        linkurl = u"http://calendar.yahoo.com/?v=60"
        linkurl += u"&TITLE="+evenement.nom
        linkurl += u"&ST="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        linkurl += u"&URL:"+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        linkurl += u"&in_loc=="+evenement.lieu.nom_lieu+u","+evenement.lieu.rue+u","+evenement.lieu.ville.nom
        linkurl += u"&DESC="+evenement.type.nom+" : "+resume(evenement.description, 150) +" "+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl =  "/static/img/evenements/40x40/yahoo-icon-40x40.png"
        return self.setLink(imgurl,linkurl)

class IcalEventLink(EventLink):
    def getLink(self,evenement):
        self.text += u" Ical"
        linkurl = reverse('event-details-ics', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl = "/static/img/evenements/40x40/ical-icon-40x40.png"
        return self.setLink(imgurl,linkurl)


def getLinkList(evenement):
    eventAddLinkList = list()
    myOutlookEventLink = OutlookEventLink()
    myGoogleEventLink = GoogleEventLink()
    myYahooEventLink = YahooEventLink()
    myIcalEventLink = IcalEventLink()
    eventAddLinkList.append(myGoogleEventLink.getLink(evenement))
    eventAddLinkList.append(myYahooEventLink.getLink(evenement))
    eventAddLinkList.append(myOutlookEventLink.getLink(evenement))
    eventAddLinkList.append(myIcalEventLink.getLink(evenement))
    return eventAddLinkList
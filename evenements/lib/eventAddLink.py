# -*- coding: utf-8 -*-
from evenements.models import Evenement
from django.core.urlresolvers import reverse
from pytz import timezone
from django.conf import settings
from valdyerresweb.templatetags.filtres import resume
import xlwt,csv
import valdyerresweb.templatetags.filtres as filtres
from StringIO import StringIO
from django.http import HttpResponse
from django.template import Context,loader
from django.utils import http



class EventLink(object):
    text =u" Ajouter à votre agenda"
    
    def getLink(self,evenement):
        raise NotImplementedError('Exception : EventLink is supposed to be an interface')
    def setLink(self,imgurl,linkurl,imgalt):
        return "<a href=\""+linkurl+"\"><img alt=\""+imgalt+"\" src=\""+imgurl+"\">"+self.text+"</a>"
    
        
class OutlookEventLink(EventLink):
    def getLink(self,evenement):
        self.text += u" Outlook"
        linkurl = reverse('event-details-ics', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl = "/static/img/evenements/40x40/outlook-icon-40x40.png"
        imgalt = "Agenda outlook"
        return self.setLink(imgurl,linkurl,imgalt)
    
class GoogleEventLink(EventLink):
    def getLink(self, evenement):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = evenement.debut
        datefin = evenement.fin
        self.text +=" Google"
        linkurl = u"&amp;action=TEMPLATE"
        linkurl += u"&amp;text="+http.urlquote_plus(evenement.nom)
        linkurl += u"&amp;dates="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        if datefin != datedebut:
            linkurl += u"/"+datefin.strftime("%Y")+datefin.strftime("%m")+datefin.strftime("%d")+u"T"+datefin.strftime("%H")+datefin.strftime("%M")+u"00Z"
        linkurl += u"&amp;sprop=website:"+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        linkurl += u"&amp;sprop=name:"+http.urlquote_plus(settings.NOM_ORGANISATION)
        linkurl += u"&amp;location="+http.urlquote_plus(evenement.lieu.nom)+u","+http.urlquote_plus(evenement.lieu.rue)+u","+http.urlquote_plus(evenement.lieu.ville.nom)
        linkurl += u"&amp;details="+http.urlquote_plus(evenement.type.nom+" : "+resume(evenement.description, 150))+"%20"+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        
        linkurl = u"http://www.google.com/calendar/event?"+linkurl
        imgurl =  "/static/img/evenements/40x40/gmail-icon-40x40.png"
        imgalt = "Agenda Google"
        return self.setLink(imgurl,linkurl,imgalt)
        
class YahooEventLink(EventLink):
    def getLink(self, evenement):
        TZone = timezone(settings.TIME_ZONE)
        datedebut = evenement.debut
        datefin = evenement.fin
        duree = datefin - datedebut
        
        self.text +=" Yahoo"
        linkurl = u"http://calendar.yahoo.com/?v=60"
        linkurl += u"&amp;TITLE="+http.urlquote_plus(evenement.nom)
        linkurl += u"&amp;ST="+datedebut.strftime("%Y")+datedebut.strftime("%m")+datedebut.strftime("%d")+u"T"+datedebut.strftime("%H")+datedebut.strftime("%M")+u"00Z"
        linkurl += u"&amp;URL:"+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        linkurl += u"&amp;in_loc=="+http.urlquote_plus(evenement.lieu.nom+u","+evenement.lieu.rue+u","+evenement.lieu.ville.nom)
        linkurl += u"&amp;DESC="+http.urlquote_plus(evenement.type.nom+" : "+resume(evenement.description, 150) +" ")+settings.NOM_DOMAINE+reverse('event-details', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl =  "/static/img/evenements/40x40/yahoo-icon-40x40.png"
        imgalt = "Agenda Yahoo"
        return self.setLink(imgurl,linkurl,imgalt)

class IcalEventLink(EventLink):
    def getLink(self,evenement):
        self.text += u" Ical"
        linkurl = reverse('event-details-ics', kwargs={'slug': evenement.cadre_evenement.slug, 'evenement_slug': evenement.slug})
        imgurl = "/static/img/evenements/40x40/ical-icon-40x40.png"
        imgalt = "Agenda Ical"
        return self.setLink(imgurl,linkurl,imgalt)


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


class EventsLink(object):
    text =u"Télécharger au format"
    
    def getLink(self,evenement):
        raise NotImplementedError('Exception : EventLink is supposed to be an interface')
    def setLink(self,imgurl,linkurl,imgalt):
        return "<a href=\""+linkurl+"\"><img alt=\""+imgalt+"\" src=\""+imgurl+"\">"+self.text+"</a>"
    
class ExcelLink(EventsLink):
    def getLink(self,dictargs):

        typeslug = dictargs['type_slug']
        period   = dictargs['period']
        orgaslug = dictargs['orga_slug']
        self.text += u" Excel"
        linkurl = reverse('export-agenda-type-period-orga', kwargs={'type_slug' :typeslug,'period' : period, 'orga_slug' : orgaslug , 'extension':'xls'})
        imgurl = "/static/img/evenements/40x40/excel-icon-40x40.png"
        imgalt = "icone excel"
        return self.setLink(imgurl,linkurl,imgalt)

class CSVLink(EventsLink):
    def getLink(self, dictargs):
       
        typeslug = dictargs['type_slug']
        period   = dictargs['period']
        orgaslug = dictargs['orga_slug']
        self.text += u" CSV"
        linkurl = reverse('export-agenda-type-period-orga', kwargs={'type_slug' :typeslug,'period' : period, 'orga_slug' : orgaslug , 'extension':'csv'})
        imgurl = "/static/img/evenements/40x40/csv-icon-40x40.png"
        imgalt = "icone CSV"
        return self.setLink(imgurl,linkurl,imgalt)
    
class ICSLink(EventsLink):
    def getLink(self, dictargs):
       
        typeslug = dictargs['type_slug']
        period   = dictargs['period']
        orgaslug = dictargs['orga_slug']
        self.text += u" Ical"
        linkurl = reverse('export-agenda-type-period-orga', kwargs={'type_slug' :typeslug,'period' : period, 'orga_slug' : orgaslug , 'extension':'ics'})
        imgurl = "/static/img/evenements/40x40/ical-icon-40x40.png"
        imgalt = "icone ICS"
        return self.setLink(imgurl,linkurl,imgalt)
    
def getEventsLinkList(dictargs):
    eventsLinkList = list()
    myExcelLink = ExcelLink()
    myCSVLink = CSVLink()
    myICSLink =ICSLink()
    eventsLinkList.append(myExcelLink.getLink(dictargs))
    eventsLinkList.append(myCSVLink.getLink(dictargs))
    eventsLinkList.append(myICSLink.getLink(dictargs))
    return eventsLinkList



class EventsSaisonLink(object):
    text =u"Télécharger au format"
    
    def getLink(self,evenement):
        raise NotImplementedError('Exception : EventLink is supposed to be an interface')
    def setLink(self,imgurl,linkurl):
        return "<a href=\""+linkurl+"\"><img src=\""+imgurl+"\">"+self.text+"</a>"


class ExcelSaisonLink(EventsLink):
    def getLink(self,saisonslug):

        self.text += u" Excel"
        linkurl = reverse('saison-details-export', kwargs={'slug' :saisonslug, 'extension':'xls'})
        imgurl = "/static/img/evenements/40x40/excel-icon-40x40.png"
        return self.setLink(imgurl,linkurl)

class CSVSaisonLink(EventsLink):
    def getLink(self,saisonslug):

        self.text += u" CSV"
        linkurl = reverse('saison-details-export', kwargs={'slug' :saisonslug, 'extension':'csv'})
        imgurl = "/static/img/evenements/40x40/csv-icon-40x40.png"
        return self.setLink(imgurl,linkurl)
    
class ICSSaisonLink(EventsLink):
    def getLink(self,saisonslug):
       
        self.text += u" Ical"
        linkurl = reverse('saison-details-export', kwargs={'slug' :saisonslug, 'extension':'ics'})
        imgurl = "/static/img/evenements/40x40/ical-icon-40x40.png"
        return self.setLink(imgurl,linkurl)


def getSaisonLinkList(saisonslug):
    SaisonLinkList = list()
    myExcelSaisonLink = ExcelSaisonLink()
    myCSVSaisonLink = CSVSaisonLink()
    myICSSaisonLink =ICSSaisonLink()
    SaisonLinkList.append(myExcelSaisonLink.getLink(saisonslug))
    SaisonLinkList.append(myCSVSaisonLink.getLink(saisonslug))
    SaisonLinkList.append(myICSSaisonLink.getLink(saisonslug))
    return SaisonLinkList

    

def GenerateExcelFile(evenements):
    myfile = StringIO()
    file_type = 'application/ms-excel'
    file_name = 'export.xls'
    
    wbk = xlwt.Workbook(encoding="UTF-8")

    sheet = wbk.add_sheet(u'agenda')
    line = 0
    mystyle = list()
    mystyle.append(xlwt.easyxf('pattern: pattern solid, fore_colour white'))
    mystyle.append(xlwt.easyxf('pattern: pattern solid, fore_colour white')) 
    
    col_width = 256 * 40
    for i in range(6):
        sheet.col(i).width = col_width
     
    for each in evenements:
        sheet.write(line, 0, each.lieu.ville.nom,mystyle[line%2])
        sheet.write(line, 1, each.nom,mystyle[line%2])
        sheet.write(line, 2, filtres.dateCustom(each.debut,each.fin),mystyle[line%2])
        sheet.write(line ,3, each.lieu.nom+" "+each.lieu.rue,mystyle[line%2])
        orgacelltxt = ""
        for orga in each.organisateur.all():
            orgacelltxt += orga.nom+" "
        
        sheet.write(line ,4, orgacelltxt,mystyle[line%2])
        url = reverse('event-details', kwargs={'slug': each.cadre_evenement.slug , 'evenement_slug': each.slug})
        url = settings.NOM_DOMAINE+url
        sheet.write(line ,5,url,mystyle[line%2])
        line = line +1
    wbk.save(myfile) 
    myfile.seek(0)     
    response = HttpResponse(myfile.read(), content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename='+file_name
    response['Content-Length'] = myfile.tell()
    return response
    
def GenerateCSVFile(evenements):
    myfile = StringIO()
    file_type = 'application/csv'
    file_name = 'export.csv'
    mycsv = csv.writer(myfile, delimiter=';', quotechar='"')
    
    for each in evenements:
        ville = each.lieu.ville.nom
        nom = each.nom
        date = each.debut.strftime("%Y-%m-%d %H:%M:%S") +"|"+ each.fin.strftime("%Y-%m-%d %H:%M:%S")
        adresse = each.lieu.nom+" "+each.lieu.rue
        orgacelltxt = ""
        for orga in each.organisateur.all():
            orgacelltxt += orga.nom+" " 
        url = reverse('event-details', kwargs={'slug': each.cadre_evenement.slug , 'evenement_slug': each.slug})
        url = settings.NOM_DOMAINE+url
        mycsv.writerow([ville.encode('UTF-8'),nom.encode('UTF-8'),date.encode('UTF-8'),adresse.encode('UTF-8'),orgacelltxt.encode('UTF-8'),url.encode('UTF-8')])
    
    myfile.seek(0)     
    response = HttpResponse(myfile.read(), content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename='+file_name
    response['Content-Length'] = myfile.tell()
    return response

def GenerateICSFile(evenements):
    file_type = 'text/calendar'
    file_name = 'export.ics'
    myTemplate = loader.get_template('evenements/multi-evenement-details.ics.html')
    myContext = Context({"liste_evenement": evenements, "settings": settings})
    text = myTemplate.render(myContext)
    response = HttpResponse(text, content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename='+file_name
    return response
    
    
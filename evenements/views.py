# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from evenements.models import *
from localisations.models import Lieu
import datetime
from django.db.models import Q
from django.template import Context,loader
from evenements.customCalendar.calendrier import CAVYCalendar, entierAvecZero
import calendar
from equipements.models import Equipement
from pytz import timezone
from valdyerresweb import settings
from django.core.urlresolvers import reverse
from model_utils.managers import InheritanceManager
from valdyerresweb.utils.functions import GenerationQrCode

utcTZ = timezone("UTC")

ListeMois = ['janvier', u'février', 'mars', 'avril', 'mai', 'juin', 'juillet', u'août', 'septembre', 'octobre', 'novembre', u'décembre']
ListeJours = ['dimanche','lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi']    


        
    

def AgendaGlobal(request):
    now = datetime.datetime.now(utcTZ)
    evenements = Evenement.objects.select_related().filter(fin__gt = now,publish = True).order_by('debut')
    typesevenements = TypeEvenement.objects.filter(evenement__fin__gt = now,evenement__publish = True).order_by('nom')
    typesevenements.query.group_by = ["id"]
    

   
    
    return render_to_response('evenements/agenda.html', {'evenements': evenements,'typeslist':typesevenements, 'typeslug':"tous" })
    
def ListType(request,type_slug):
    now = datetime.datetime.now(utcTZ)
    typeevenement = TypeEvenement.objects.get(slug=type_slug)
    typesevenements = TypeEvenement.objects.filter(evenement__fin__gt = now,evenement__publish = True).order_by('nom')
    typesevenements.query.group_by = ["id"]
    
    evenements = Evenement.objects.select_related().filter(fin__gt = now,publish = True,type = typeevenement.id).order_by('debut')
    
    return render_to_response('evenements/agenda.html', {'evenements': evenements, 'typeslist':typesevenements , 'typeslug':type_slug})

def ListAllType(request):
    now = datetime.datetime.now(utcTZ)
    typesevenements = TypeEvenement.objects.filter(evenement__fin__gt = now,evenement__publish = True).order_by('nom')
    typesevenements.query.group_by = ["id"]

    return render_to_response('evenements/agenda-list-type-orga-saison.html',{'typeslist':typesevenements})
    
def AgendaMois(request, annee, mois):
    try:
        month = int(mois)
        year = int(annee)
        
        mois = entierAvecZero(month)
        
        if month == 1:
            mois_prec = '12'
            annee_prec = str(year-1)
        else:
            annee_prec = str(year)
            mois_prec = entierAvecZero(month-1)
            

        if month == 12:
            mois_suiv = '01'
            annee_suiv = str(year+1)
        else:
            mois_suiv = entierAvecZero(month+1)
            annee_suiv = str(year)
    
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.datetime(year, month, dayStart,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, month, dayEnd,23,59,0,tzinfo=utcTZ)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        evenements = list()
        
        nbre_evenement = 0
        for each in liste_event:
            evenements.append(each)
            nbre_evenement = nbre_evenement+1
            
        CAVYcalendrier = CAVYCalendar(evenements)

        calendrier = CAVYcalendrier.formatmonth(year, month)
        
        now ="False"
        
    except Saison.DoesNotExist:
        raise Http404
    return render_to_response('evenements/calendrier.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv, 'now': now, 'mois': mois, 'annee': year, 'nbre_evenement': nbre_evenement})

def AgendaMoisICS(request, annee, mois):
    try:
        month = int(mois)
        year = int(annee)
    
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.datetime(year, month, dayStart,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, month, dayEnd,23,59,0,tzinfo=utcTZ)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
    
        evenements = list()   
        for each in liste_event:
            evenements.append(each)
            
        myText = MultiEvenementsDetailsIcalendar(evenements)
        
    except Saison.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")

def AgendaAnnee(request, annee):
    try:
        year = int(annee)
        
        DateDebut = datetime.datetime(year, 1, 1,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, 12, 31,23,59,tzinfo=utcTZ)
        evenements = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin).filter(publish=1).order_by('debut')
        liste_lieux = Lieu.objects.select_related().select_subclasses().all()
        
        listeLieux = {}
        for each in liste_lieux:
            listeLieux[each.id] = each

        liste_evenements = list()
        for each in evenements:
            each.lieu = listeLieux[each.lieu_id]
            liste_evenements.append(each)
            
        listeHtml = list()
        
        TZone = timezone(settings.TIME_ZONE)
        debut = liste_evenements[0].debut.astimezone(TZone)
        
        mois = int(debut.strftime("%m"));
            
        listeHtml.append('<li>'+ListeMois[mois]+'<ul>')
        
        if type(liste_evenements[0].lieu) == Equipement:
            lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': liste_evenements[0].lieu.fonction.slug, 'equipement_slug': liste_evenements[0].lieu.slug})+'">'+liste_evenements[0].lieu.nom_lieu+'</a> - '
        else:
            lien = ''
        
        listeHtml.append('<li>'+ListeJours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" - "+debut.strftime("%H")+"h"+debut.strftime("%M")+" : <a href=\""+reverse('event-details', kwargs={'slug': liste_evenements[0].cadre_evenement.slug, 'evenement_slug': liste_evenements[0].slug})+"\">"+liste_evenements[0].nom+"</a> | "+lien+liste_evenements[0].lieu.ville.nom+"</li>")
        
        liste_evenements.remove(liste_evenements[0])
        
        for each in liste_evenements:
            TZone = timezone(settings.TIME_ZONE)
            debut = each.debut.astimezone(TZone)
            
            if int(debut.strftime("%m")) != mois:
                mois = int(debut.strftime("%m"))
                listeHtml.append("</ul></li><li>"+ListeMois[mois]+"<ul>")
                
            if type(each.lieu) == Equipement:
                lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': each.lieu.fonction.slug, 'equipement_slug': each.lieu.slug})+'">'+each.lieu.nom_lieu+'</a> - '
            else:
                lien = ''
            
            listeHtml.append('<li>'+ListeJours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" - "+debut.strftime("%H")+"h"+debut.strftime("%M")+" : <a href=\""+reverse('event-details', kwargs={'slug': each.cadre_evenement.slug, 'evenement_slug': each.slug})+"\">"+each.nom+"</a> | "+lien+each.lieu.ville.nom+"</li>")
        
        listeHtml.append('</ul>')
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda-annee.html', {'liste_evenement': listeHtml, 'annee': annee})

def AgendaAnneeICS(request, annee):
    try:
        year = int(annee)
        
        DateDebut = datetime.datetime(year, 1, 1,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, 12, 31,23,59,tzinfo=utcTZ)
        evenements = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin).filter(publish=1).order_by('debut')

        liste_evenements = list()
        for each in evenements:
            liste_evenements.append(each)
        
        myText = MultiEvenementsDetailsIcalendar(liste_evenements)
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")

def AgendaNow(request):
    try:
        month = datetime.datetime.now(utcTZ).month
        year = datetime.datetime.now(utcTZ).year
        
        if month == 1:
            mois_prec = '12'
            annee_prec = str(year-1)
        else:
            annee_prec = str(year)
            mois_prec = entierAvecZero(month-1)
            

        if month == 12:
            mois_suiv = '01'
            annee_suiv = str(year+1)
        else:
            mois_suiv = entierAvecZero(month+1)
            annee_suiv = str(year)
        
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.datetime(year, month, dayStart,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, month, dayEnd,23,59,0,tzinfo=utcTZ)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        evenements = list()
        
        saisons = SaisonCulturelle.objects.filter(fin__gt=datetime.datetime.now(utcTZ))
        listeFestival = list()
        
        for each in saisons:
            festivals = Festival.objects.select_related().filter(saison_culture_id=each.id)
            for eachFestival in festivals:
                listeFestival.append(eachFestival)
        
        nbre_evenement = 0  
        for each in liste_event:
            evenements.append(each)
            nbre_evenement = nbre_evenement+1
        
        
        CAVYcalendrier = CAVYCalendar(evenements)
        calendrier = CAVYcalendrier.formatmonth(year, month)
        
        now = "True"
    except Saison.DoesNotExist:
        raise Http404
    return render_to_response('evenements/calendrier.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv, 'now': now, 'nbre_evenement': nbre_evenement})

def AgendaNowICS(request):
    try:
        month = datetime.datetime.now(utcTZ).month
        year = datetime.datetime.now(utcTZ).year
        
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.datetime(year, month, dayStart,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.datetime(year, month, dayEnd,23,59,0,tzinfo=utcTZ)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        
        evenements = list()    
        for each in liste_event:
            evenements.append(each)
        
        myText = MultiEvenementsDetailsIcalendar(evenements)
    except Saison.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")

def SaisonDetailsHtml(request, slug):
    try:
        saison = Saison.objects.select_related().select_subclasses().get(slug=slug)

        if type(saison) == Festival:
            evenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
            isfestival = "True"
        else:
            Qevenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1)
            festival = Festival.objects.select_related().filter(saison_culture_id=saison.id)
            
            filtre = Q(cadre_evenement_id=saison.id)
            for each in festival:
                filtre.add(Q(cadre_evenement_id=each.id), 'OR')
                
            evenements = Qevenements.order_by('debut').filter(filtre)
            isfestival = "False"

        liste_lieux = Lieu.objects.select_related().select_subclasses().all()
        
        listeLieux = {}
        for each in liste_lieux:
            listeLieux[each.id] = each

        liste_evenements = list()
        for each in evenements:
            each.lieu = listeLieux[each.lieu_id]
            liste_evenements.append(each)
            
        listeHtml = list()
        
        TZone = timezone(settings.TIME_ZONE)
        debut = liste_evenements[0].debut.astimezone(TZone)
        
        mois = int(debut.strftime("%m"));
            
        listeHtml.append('<li>'+ListeMois[mois]+' - '+debut.strftime("%Y")+'<ul>')
        
        if type(liste_evenements[0].lieu) == Equipement:
            lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': liste_evenements[0].lieu.fonction.slug, 'equipement_slug': liste_evenements[0].lieu.slug})+'">'+liste_evenements[0].lieu.nom_lieu+'</a> - '
        else:
            lien = ''
            
        listeHtml.append('<li>'+ListeJours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" - "+debut.strftime("%H")+"h"+debut.strftime("%M")+" : <a href=\""+reverse('event-details', kwargs={'slug': liste_evenements[0].cadre_evenement.slug, 'evenement_slug': liste_evenements[0].slug})+"\">"+liste_evenements[0].nom+"</a> | "+lien+liste_evenements[0].lieu.ville.nom+"</li>")
        
        liste_evenements.remove(liste_evenements[0])
        
        for each in liste_evenements:
            TZone = timezone(settings.TIME_ZONE)
            debut = each.debut.astimezone(TZone)
            
            if int(debut.strftime("%m")) != mois:
                mois = int(debut.strftime("%m"))
                listeHtml.append("</ul></li><li>"+ListeMois[mois]+" - "+debut.strftime("%Y")+"<ul>")
                
            if type(each.lieu) == Equipement:
                lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': each.lieu.fonction.slug, 'equipement_slug': each.lieu.slug})+'">'+each.lieu.nom_lieu+'</a> - '
            else:
                lien = ''
            
            listeHtml.append('<li>'+ListeJours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" - "+debut.strftime("%H")+"h"+debut.strftime("%M")+" : <a href=\""+reverse('event-details', kwargs={'slug': each.cadre_evenement.slug, 'evenement_slug': each.slug})+"\">"+each.nom+"</a> | "+lien+each.lieu.ville.nom+"</li>")
        
        listeHtml.append('</ul>')
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/saison-details.html', {'liste_evenement': listeHtml, 'saison': saison, 'isfestival': isfestival, 'evenements': evenements})

def SaisonDetailsICS(request, slug):
    try:
        saison = Saison.objects.select_related().select_subclasses().get(slug=slug)

        if type(saison) == Festival:
            evenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
        else:
            Qevenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1)
            festival = Festival.objects.select_related().filter(saison_culture_id=saison.id)
            
            filtre = Q(cadre_evenement_id=saison.id)
            for each in festival:
                filtre.add(Q(cadre_evenement_id=each.id), 'OR')
                
            evenements = Qevenements.order_by('debut').filter(filtre)

        liste_evenements = list()
        for each in evenements:
            liste_evenements.append(each)
        
        myText = MultiEvenementsDetailsIcalendar(evenements)
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")

def EvenementDetailsIcalendar(evenement):
    myTemplate = loader.get_template('evenements/evenement-details.ics.html')
    myContext = Context({"evenement": evenement, "settings": settings})
    return myTemplate.render(myContext)

def MultiEvenementsDetailsIcalendar(evenements):
    myTemplate = loader.get_template('evenements/multi-evenement-details.ics.html')
    myContext = Context({"liste_evenement": evenements, "settings": settings})
    return myTemplate.render(myContext)
    
    


def EvenementDetailsHtml(request, slug, evenement_slug):
    try:
        saison = Saison.objects.select_related().select_subclasses().get(slug=slug)
        evenement = Evenement.objects.select_related().get(slug=evenement_slug)
        tarifs = Tarification.objects.filter(evenement_id=evenement.id)
        evenement_qr = GenerationQrCode(EvenementDetailsIcalendar(evenement))
        evenement.lieu = Lieu.objects.select_subclasses().get(id=evenement.lieu.id)
        
        festival = None
        if type(saison) == Festival:
            festival = saison
            saison = festival.saison_culture

        localisation_qr = GenerationQrCode("geo:"+str(evenement.lieu.latitude)+","+str(evenement.lieu.longitude))

        #<trash>
        try:
            tarifs = tarifs[0]
        except:
            tarifs = None
        #</trash>  
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/evenement-details.html', {'evenement': evenement, 'saison': saison, 'festival':festival , 'tarifs': tarifs, 'evenement_qr': evenement_qr, 'localisation_qr': localisation_qr })



def EvenementDetailsICS(request, slug, evenement_slug, festival_slug = None):
    try:
        evenement = Evenement.objects.select_related(depth=1).get(slug=evenement_slug)
        myText = EvenementDetailsIcalendar(evenement)
    except Evenement.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")
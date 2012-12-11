# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response , redirect , get_object_or_404
from evenements.models import *
from django.db.models import Q
from django.template import Context,loader
from evenements.customCalendar.calendrier import CAVYCalendar, entierAvecZero
import calendar,datetime
from equipements.models import Equipement
from pytz import timezone
from valdyerresweb import settings
from django.core.urlresolvers import reverse
from valdyerresweb.utils.functions import GenerationQrCode
from evenements.lib.eventAddLink import GenerateExcelFile, GenerateCSVFile, GenerateICSFile
from django.views.decorators.cache import cache_page



utcTZ = timezone("UTC")
myTimezone = timezone(settings.TIME_ZONE)

ListeMois = ['janvier', u'février', 'mars', 'avril', 'mai', 'juin', 'juillet', u'août', 'septembre', 'octobre', 'novembre', u'décembre']
ListeJours = ['dimanche','lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi']    

#compatibilité datetime
WeekDay = ['lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi','dimanche']    



        
    

def AgendaGlobal(request, type_slug = 'tous',period = 'toutes', orga_slug = 'tous'):
    now = datetime.datetime.now(utcTZ)
    evenements = Evenement.objects.select_related().filter(fin__gt = now,publish = True).order_by('debut')
    typesevenements = TypeEvenement.objects.filter(evenement__fin__gt = now,evenement__publish = True).order_by('nom')
    typesevenements.query.group_by = ["id"]
    
    organisateurs = Organisateur.objects.filter(evenement__fin__gt = datetime.datetime.now(utcTZ) ,evenement__publish = True).order_by('nom')
    organisateurs.query.group_by = ["id"]
     
    type_slug = 'tous'
    period = 'toutes'
    orga_slug = 'tous'
    dictargs = {}
    dictargs['type_slug']=type_slug
    dictargs['period']=period
    dictargs['orga_slug']=orga_slug
    
    return render_to_response('evenements/agenda.html', {'evenements': evenements, 'typeslist':typesevenements ,'orgalist':organisateurs ,'typeslug':type_slug , 'orgaslug':orga_slug  , 'period':period,'dictargs':dictargs})
    

def AgendaListTypePeriodOrga(request,type_slug = 'tous',period = 'toutes', orga_slug = 'tous', export=False ):
    midnight = datetime.time(23, 59, 59)
    startDate = datetime.datetime.now(utcTZ)
    if (type_slug == 'tous') and (period == 'toutes') and (orga_slug == 'tous') and (export == False):
        return redirect('agenda-global')
    dictargs = {}
    dictargs['type_slug']=type_slug
    dictargs['period']=period
    dictargs['orga_slug']=orga_slug
    
    print period
    
    if period == "cette-semaine":
        print 'hello\n'
        endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()) )
        if startDate.weekday() == 6:
            endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()-1), weeks=1 )
        endDate = datetime.datetime.combine(endDate.date(),midnight)
        endDate.replace(tzinfo=utcTZ)
        print startDate + datetime.timedelta(days=(6-startDate.weekday()) )
    
    if period == "ce-week-end":
        startDate = startDate + datetime.timedelta(days=(4-startDate.weekday()) )
        endafternoon = datetime.time(17, 30, 00)
        startDate = datetime.datetime.combine(startDate.date(),endafternoon)
        
        endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()) )
        if startDate.weekday() == 6:
            endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()-1), weeks=1 )
        endDate = datetime.datetime.combine(endDate.date(),midnight)
        endDate.replace(tzinfo=utcTZ)
        
            
    if period == "ce-mois":
        endDate = datetime.datetime(startDate.year,startDate.month,calendar.monthrange(startDate.year, startDate.month)[1],0,0,0,tzinfo=myTimezone)
        endDate = datetime.datetime.combine(endDate.date(),midnight)
    
    typesevenements = TypeEvenement.objects.filter(evenement__fin__gt = datetime.datetime.now(utcTZ) ,evenement__publish = True).order_by('nom')
    typesevenements.query.group_by = ["id"]
    
    organisateurs = Organisateur.objects.filter(evenement__fin__gt = datetime.datetime.now(utcTZ) ,evenement__publish = True).order_by('nom')
    organisateurs.query.group_by = ["id"]
    
    evenements = Evenement.objects.select_related().filter(fin__gt = startDate ,publish = True).order_by('debut')
    evenements.prefetch_related('organisateur')
    if period !="toutes":
        evenements =  evenements.filter(debut__lt = endDate )
    
    if type_slug != "tous" :
        typeevenement = TypeEvenement.objects.get(slug=type_slug)
        evenements =  evenements.filter(type = typeevenement.id)
    if orga_slug != "tous" :
        organisateur = Organisateur.objects.get(slug=orga_slug)    
        evenements =  evenements.filter(organisateur = organisateur.id)
    if export == True:
        return evenements
    flash = None    
    if len(evenements) == 0:
        flash = u"Il n'y a pas d'évènement à venir : <ul>"
        if type_slug != "tous":
            flash += u"<li>De type "+typeevenement.nom+".</li>"
        if period != u"toutes":
            flash += u"<li>Pour la période comprise entre le "+ WeekDay[startDate.weekday()] + u" "+ str(startDate.day) +u" "+ListeMois[startDate.month-1]+" "
            flash += u"et le "+ WeekDay[endDate.weekday()]+ u" "+ str(endDate.day) +u" "+ListeMois[endDate.month-1]+".</li>"
        if orga_slug != u"tous":
            flash += u"<li>Organisé par "+ organisateur.nom+".</li>"
        flash += u"<ul>" 
    
    return render_to_response('evenements/agenda.html', {'evenements': evenements, 'typeslist':typesevenements ,'orgalist':organisateurs ,'typeslug':type_slug , 'orgaslug':orga_slug  , 'period':period , 'flash':flash,'dictargs':dictargs})


def ExportAgendaListTypePeriodOrga(request,type_slug = 'tous',period = 'toutes', orga_slug = 'tous', extension = 'meuh' ):
    evenements = AgendaListTypePeriodOrga(request, type_slug, period, orga_slug,True)
    if extension == 'xls':
        response = GenerateExcelFile(evenements)
    elif extension == 'csv':
        response = GenerateCSVFile(evenements)
    elif extension == 'ics':
        response = GenerateICSFile(evenements)
    else:
        raise Http404
    return response

def OrganisateurDetailsHtml(request,organisateur_slug):
    try:
        organisateur = Organisateur.objects.get(slug=organisateur_slug)
        organisateur_qr = GenerationQrCode(OrganisateurVcard(organisateur))
    except OrganisateurDetailsHtml.DoesNotExist:
        raise Http404
    
    return render_to_response('evenements/organisateur-details.html', {'organisateur': organisateur , 'organisateur_qr':organisateur_qr })

def OrganisateurVCF(request, organisateur_slug):
    try:
        organisateur = Organisateur.objects.get(slug=organisateur_slug)
        
        myText = OrganisateurVcard(organisateur)
    except Lieu.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/vcard")

def OrganisateurVcard(organisateur):
    myTemplate = loader.get_template('evenements/organisateur.vcf.html')
    myContext = Context({"organisateur": organisateur, "settings": settings})
    return myTemplate.render(myContext)

def SaisonDetailsHtml(request,slug):
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses() , slug = slug)
    festival = None
     
    if type(saison) == Festival:
        evenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
        evenementspasses =  Evenement.objects.select_related().filter(fin__lt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
        festival = saison
        saison = festival.saison_culture
    else:
        Qevenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1)
        QevenementsPast = Evenement.objects.select_related().filter(fin__lt=datetime.datetime.now(utcTZ)).filter(publish=1)
        festivals = Festival.objects.select_related().filter(saison_culture_id=saison.id)
            
        filtre = Q(cadre_evenement_id=saison.id)
        for each in festivals:
            filtre.add(Q(cadre_evenement_id=each.id), 'OR')
                
        evenements = Qevenements.order_by('debut').filter(filtre)
        evenementspasses = QevenementsPast.order_by('debut').filter(filtre)
        


        
    return render_to_response('evenements/agenda-saison.html', {'saison' : saison ,'evenements':evenements , 'evenementspasses':evenementspasses ,'festival':festival })

def SaisonDetailsHtmlExport(request,slug,extension):
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses() , slug = slug)
    festival = None
     
    if type(saison) == Festival:
        evenements = Evenement.objects.select_related().filter(publish=1).filter(cadre_evenement_id=saison.id)
       
        festival = saison
        saison = festival.saison_culture
    else:
        Qevenements = Evenement.objects.select_related().filter(publish=1)
        festivals = Festival.objects.select_related().filter(saison_culture_id=saison.id)
            
        filtre = Q(cadre_evenement_id=saison.id)
        for each in festivals:
            filtre.add(Q(cadre_evenement_id=each.id), 'OR')
                
        evenements = Qevenements.order_by('debut').filter(filtre)
        
    if extension == 'xls':
        response = GenerateExcelFile(evenements)
    elif extension == 'csv':
        response = GenerateCSVFile(evenements)
    elif extension == 'ics':
        response = GenerateICSFile(evenements)
    else:
        raise Http404
    return response

 
def SaisonDetailsHtmlOld(request, slug):
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
            lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': liste_evenements[0].lieu.fonction.slug, 'equipement_slug': liste_evenements[0].lieu.slug})+'">'+liste_evenements[0].lieu.nom+'</a> - '
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
                lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': each.lieu.fonction.slug, 'equipement_slug': each.lieu.slug})+'">'+each.lieu.nom+'</a> - '
            else:
                lien = ''
            
            listeHtml.append('<li>'+ListeJours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" - "+debut.strftime("%H")+"h"+debut.strftime("%M")+" : <a href=\""+reverse('event-details', kwargs={'slug': each.cadre_evenement.slug, 'evenement_slug': each.slug})+"\">"+each.nom+"</a> | "+lien+each.lieu.ville.nom+"</li>")
        
        listeHtml.append('</ul>')
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/saison-details.html', {'liste_evenement': listeHtml, 'saison': saison, 'isfestival': isfestival, 'evenements': evenements})



    
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
            lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': liste_evenements[0].lieu.fonction.slug, 'equipement_slug': liste_evenements[0].lieu.slug})+'">'+liste_evenements[0].lieu.nom+'</a> - '
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
                lien = '<a href="'+reverse('equipement-details', kwargs={'fonction_slug': each.lieu.fonction.slug, 'equipement_slug': each.lieu.slug})+'">'+each.lieu.nom+'</a> - '
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
        evenement = Evenement.objects.select_related().prefetch_related('organisateur').get(slug=evenement_slug)
        saison = Saison.objects.select_related().select_subclasses().get(slug=slug)
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
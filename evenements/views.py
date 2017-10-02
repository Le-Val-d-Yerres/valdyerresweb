# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response , redirect , get_object_or_404
from evenements.models import *
from django.db.models import Q
from django.template import loader
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
ListeJours = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
# compatibilité datetime
WeekDay = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']


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
    
    AllowPeriode = ['toutes', 'cette-semaine', 'ce-week-end', 'ce-mois']
    
    if period not in AllowPeriode:
        raise Http404
    
    if period == "cette-semaine":
        endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()) )
        if startDate.weekday() == 6:
            endDate = startDate + datetime.timedelta(days=(6-startDate.weekday()-1), weeks=1 )
        endDate = datetime.datetime.combine(endDate.date(),midnight)
        endDate.replace(tzinfo=utcTZ)
    
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
        typeevenement = get_object_or_404(TypeEvenement,slug=type_slug)
        evenements =  evenements.filter(type = typeevenement.id)
    if orga_slug != "tous" :
        organisateur = get_object_or_404(Organisateur,slug=orga_slug)    
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
    organisateur = get_object_or_404(Organisateur.objects.select_related(), slug=organisateur_slug)

    
    if organisateur.orga_service != None:
        return redirect('/services/'+organisateur.orga_service.slug)
    elif organisateur.orga_equipement != None:
        return redirect(organisateur.orga_equipement.get_absolute_url())
    
    
    organisateur_qr = GenerationQrCode(OrganisateurVcard(organisateur))
    
    return render_to_response('evenements/organisateur-details.html', {'organisateur': organisateur , 'organisateur_qr':organisateur_qr })

def OrganisateurVCF(request, organisateur_slug):

    organisateur = get_object_or_404(Organisateur.objects, slug=organisateur_slug)
    
    myText = OrganisateurVcard(organisateur)

    return HttpResponse(myText,content_type="text/vcard")

def OrganisateurVcard(organisateur):
    myTemplate = loader.get_template('evenements/organisateur.vcf.html')
    myContext = {"organisateur": organisateur, "settings": settings}
    return myTemplate.render(myContext)

def SaisonDetailsHtml(request,slug):
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses() , slug = slug)
    festival = None
     
    if type(saison) == Festival:
        evenements = Evenement.objects.select_related().filter(fin__gt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
        evenementspasses =  Evenement.objects.select_related().filter(fin__lt=datetime.datetime.now(utcTZ)).filter(publish=1).filter(cadre_evenement_id=saison.id)
        festival = saison
        saison = festival.saison_culture
        evenements = evenements.order_by('debut')

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
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses(), slug=slug)

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
        
    return render_to_response('evenements/saison-details.html', {'liste_evenement': listeHtml, 'saison': saison, 'isfestival': isfestival, 'evenements': evenements})



    
def AgendaMois(request, annee, mois):
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
        
    return render_to_response('evenements/calendrier.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv, 'now': now, 'mois': mois, 'annee': year, 'nbre_evenement': nbre_evenement})

def AgendaMoisICS(request, annee, mois):
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

    return HttpResponse(myText,content_type="text/calendar")

def AgendaAnnee(request, annee):
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
    return render_to_response('evenements/agenda-annee.html', {'liste_evenement': listeHtml, 'annee': annee})

def AgendaAnneeICS(request, annee):
    year = int(annee)
    
    DateDebut = datetime.datetime(year, 1, 1,0,0,0,tzinfo=utcTZ)
    DateFin = datetime.datetime(year, 12, 31,23,59,tzinfo=utcTZ)
    evenements = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin).filter(publish=1).order_by('debut')

    liste_evenements = list()
    for each in evenements:
        liste_evenements.append(each)
    
    myText = MultiEvenementsDetailsIcalendar(liste_evenements)
    return HttpResponse(myText,content_type="text/calendar")

def AgendaNow(request):
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
    return render_to_response('evenements/calendrier.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv, 'now': now, 'nbre_evenement': nbre_evenement})

def AgendaNowICS(request):
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
    return HttpResponse(myText,content_type="text/calendar")



def SaisonDetailsICS(request, slug):
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses(), slug=slug)

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
    return HttpResponse(myText,content_type="text/calendar")

def EvenementDetailsIcalendar(evenement):
    myTemplate = loader.get_template('evenements/evenement-details.ics.html')
    myContext = {"evenement": evenement, "settings": settings}
    return myTemplate.render(myContext)

def MultiEvenementsDetailsIcalendar(evenements):
    myTemplate = loader.get_template('evenements/multi-evenement-details.ics.html')
    myContext = {"liste_evenement": evenements, "settings": settings}
    return myTemplate.render(myContext)
    
    
def EvenementDetailsHtml(request, slug, evenement_slug):
    evenement = get_object_or_404(Evenement.objects.select_related().prefetch_related('organisateur').filter(publish=True), slug=evenement_slug)
    saison = get_object_or_404(Saison.objects.select_related().select_subclasses(), slug=slug)
    if evenement.cadre_evenement.id != saison.id:
        raise Http404
    
    evenement_qr = GenerationQrCode(EvenementDetailsIcalendar(evenement))
    evenement.lieu = Lieu.objects.select_subclasses().get(id=evenement.lieu.id)
    tarification = Prix.objects.filter(evenement = evenement.id).order_by('prix')
    documentattache = DocumentAttache.objects.filter(reference = evenement.id)
    festival = None
    if type(saison) == Festival:
        festival = saison
        saison = festival.saison_culture

    localisation_qr = GenerationQrCode("geo:"+str(evenement.lieu.latitude)+","+str(evenement.lieu.longitude))
# calcul événement passé
    a_venir = False
    maintenant = datetime.datetime.utcnow()
    maintenant = maintenant.replace(tzinfo=utcTZ)
    if evenement.fin > maintenant:
        a_venir = True

    return render_to_response('evenements/evenement-details.html', {'evenement': evenement, 'saison': saison, 'festival':festival ,'tarification':tarification,'documentattache':documentattache, 'evenement_qr': evenement_qr, 'localisation_qr': localisation_qr, 'a_venir':a_venir })


def EvenementDetailsICS(request, slug, evenement_slug, festival_slug = None):
    evenement = get_object_or_404(Evenement.objects.select_related(), slug=evenement_slug)
    myText = EvenementDetailsIcalendar(evenement)
    return HttpResponse(myText, content_type="text/calendar")


def OrganisateurRedirect(request):
    return redirect('agenda-global')


def AgendaTypeRedirect(request):
    return redirect('agenda-global')


def AgendaPeriodRedirect(request, type_slug):
    return redirect('agenda-type-period-orga', type_slug=type_slug, period='toutes')


def AgendaOrgaRedirect(request, type_slug, period):
    return redirect('agenda-type-period-orga', type_slug=type_slug, period=period, orga_slug='tous')
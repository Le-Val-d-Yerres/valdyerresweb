from django.http import Http404
from django.shortcuts import render_to_response
from evenements.models import *
from datetime import datetime
from django.db.models import Q

def Agenda(request):
    try:
        liste_saisons = Saison.objects.filter(fin__gt=datetime.now())
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda.html', {'liste_evenement': liste_saisons})

def SaisonDetailsHtml(request, saison_slug):
    try:
        saison = Saison.objects.get(slug=saison_slug)
        festival = Festival.objects.filter(saison_culture_id=saison.id)
        evenements = Evenement.objects.filter(fin__gt=datetime.now()).filter(publish=1)
        
        filtre = Q(cadre_evenement_id=saison.id)
        for each in festival:
            filtre.add(Q(cadre_evenement_id=each.id), 'OR')
            
        liste_evenement = evenements.order_by('-haut_page').filter(filtre)
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/saison-details.html', {'liste_evenement': liste_evenement, 'saison': saison})

def SaisonEvenementDetailsHtml(request):
    return True

def SaisonFestivalEvenementDetailsHtml(request):
    return True

def SaisonFestivalDetailsHtml(request, saison_slug, festival_slug):
    try:
        saison = SaisonCulturelle.objects.get(slug=saison_slug)
        details_festival = Festival.objects.get(slug=festival_slug)
        liste_evenement = Evenement.objects.filter(cadre_evenement_id=details_festival.id)
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/festival-details.html', {'liste_evenement': liste_evenement, 'details_festival' : details_festival, 'saison' : saison})
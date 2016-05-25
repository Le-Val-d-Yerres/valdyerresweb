# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect, get_object_or_404, \
    get_list_or_404
from editorial.models import Magazine, RapportActivite, Actualite, DocumentAttache, PageBase, PageStatique, \
    NewsletterBib
from cinemas.models import Seance
from evenements.models import Evenement
from equipements.models import Equipement
from horaires.models import Horaires, Periode, Jour
from pytz import timezone, tzinfo
from datetime import date
from valdyerresweb import settings
import datetime
from django.views.decorators.cache import cache_control, cache_page
from annoncesemploi.models import Annonce
from django import forms
from django.template import RequestContext
from valdyerresweb.utils import functions
import uuid

myTZ = timezone(settings.TIME_ZONE)
utcTZ = timezone("UTC")


def Home(request):
    today = date.today()

    startdate = datetime.datetime.combine(today, datetime.time(00, 00, 01))
    enddate = datetime.datetime.combine(today, datetime.time(23, 59, 59))

    startdate = startdate.replace(tzinfo=utcTZ)
    enddate = enddate.replace(tzinfo=utcTZ)

    actualites = Actualite.objects.filter(publie=True, page_accueil=True).order_by('-date_publication')[0:4]
    evenements_une_lg1 = Evenement.objects.filter(page_accueil=False, publish=True, fin__gt=startdate).order_by(
        'debut')[0:5]
    evenements_une_lg2 = Evenement.objects.filter(page_accueil=True, publish=True, fin__gt=startdate).order_by('debut')[
                         0:3]
    carroussel = PageBase.objects.filter(publie=True, carroussel=True).select_subclasses().order_by('index_carroussel')

    # nb de seances de vinéma aujourd'hui
    cinema_count = Seance.objects.filter(date_debut__gt=startdate, date_fin__lt=enddate).count()
    # nb d'evenements aujourd'hui
    # evenements_count = Evenement.objects.filter(publish=True,debut__gt = startdate, fin__lt = enddate).count()
    evenements_count = Evenement.objects.filter(fin__gt=startdate, debut__lt=enddate, publish=True).count()

    # nb d'equipements ouverts aujourd'hui
    equipements = Equipement.objects.all()

    listhoraires = list()

    for equipement in equipements:
        periodes = Periode.objects.filter(date_debut__lte=today, date_fin__gte=today).filter(
            horaires__equipement=equipement.id).order_by('date_debut')
        if len(periodes) >= 1:
            periodes.query.group_by = ['periode_id']
            periode_active = periodes[len(periodes) - 1]
            horaires = Horaires.objects.select_related().filter(equipement=equipement.id).filter(
                periodes__id=periode_active.id)
            listhoraires.append(horaires)

    numjour = today.isoweekday()
    equipements_ouverts = list()
    for horaires in listhoraires:
        for horaire in horaires:
            myJour = horaire.GetDay(numjour)
            if myJour.matin_ferme and myJour.am_ferme:
                continue
            else:
                if horaire.equipement not in equipements_ouverts:
                    equipements_ouverts.append(horaire.equipement)

    equipements_count = len(equipements_ouverts)
    # dernier magazine

    magazine = Magazine.objects.filter(publie=True).order_by('-date_parution')[0]

    # nb annonces emploi
    annoncesemploi = Annonce.objects.select_related().filter(publie=True).order_by('service')

    # noubliez-pas

    notes = PageStatique.objects.filter(publie=True, note_page_accueil=True)

    tokenCSRF = uuid.uuid1()

    reponse = render_to_response('editorial/home.html',
                                 {'token': tokenCSRF, 'carroussel': carroussel, 'actualites': actualites,
                                  'cinema_count': cinema_count, 'evenements_count': evenements_count,
                                  'equipements_count': equipements_count, 'magazine': magazine,
                                  'annoncesemploi': annoncesemploi, 'notes': notes,
                                  'evenements_une_lg1': evenements_une_lg1, 'evenements_une_lg2': evenements_une_lg2})
    reponse.set_cookie("csrftoken", tokenCSRF, 60 * 5)

    return reponse


def ActuList(request):
    pages = get_list_or_404(Actualite.objects.order_by('-date_publication'))

    paginator = Paginator(pages, 6)
    page = request.GET.get('page')

    try:
        if page == None:
            pages = paginator.page(1)
        elif page == "":
            return redirect('actu-list')
        elif int(page) == 1:
            return redirect('actu-list')
        else:
            pages = paginator.page(page)
    except ValueError:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response('editorial/actualite-list.html', {'pages': pages})


def ActuDetail(request, actualite_slug):
    page = get_object_or_404(Actualite.objects.filter(publie=True), slug=actualite_slug)
    documentattache = DocumentAttache.objects.filter(reference=page.id)
    return render_to_response('editorial/actualite.html', {'page': page, 'documentattache': documentattache})


def PageDetail(request, page_slug):
    page = get_object_or_404(PageStatique.objects.filter(publie=True), slug=page_slug)
    documentattache = DocumentAttache.objects.filter(reference=page.id)
    return render_to_response('editorial/page-statique.html', {'page': page, 'documentattache': documentattache})


def Magazines(request):
    magazines_list = Magazine.objects.filter(publie=True).order_by('-date_parution')
    paginator = Paginator(magazines_list, 5)
    page = request.GET.get('page')

    try:
        if page is None:
            magazines = paginator.page(1)
            page = 1
        elif page == "":
            return redirect('magazines')
        elif int(page) == 1:
            return redirect('magazines')
        else:
            magazines = paginator.page(page)
    except ValueError:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response('editorial/magazines.html', {'magazines': magazines, 'page': page})


def Rapports(request):
    rapports_list = RapportActivite.objects.filter(publie=True).order_by('-date_parution')
    paginator = Paginator(rapports_list, 5)
    page = request.GET.get('page')

    try:
        if page is None:
            rapports = paginator.page(1)
            page = 1
        elif page == "":
            return redirect('rapports')
        elif int(page) == 1:
            return redirect('rapports')
        else:
            rapports = paginator.page(page)
    except ValueError:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response('editorial/rapports.html', {'rapports': rapports, 'page': page})


def Ephemeride(request, jour='aujourd-hui'):
    jourdate = jour.split('-')
    datepage = date.today()

    if len(jourdate) == 3:
        tmpdate = datetime.datetime.strptime(jour, "%d-%m-%Y").date()
        delta = (tmpdate - datepage)
        if tmpdate == datepage:
            return redirect('ephemeride', 'aujourd-hui')
        if delta.days == 1:
            return redirect('ephemeride', 'demain')
        if delta.days <= -1:
            return redirect('ephemeride', 'aujourd-hui')
        if delta.days > 9:
            return redirect('ephemeride', 'aujourd-hui')
        datepage = tmpdate

    elif jour == "aujourd-hui":
        datepage = date.today()
    elif jour == "demain":
        delta = datetime.timedelta(days=1)
        datepage = datepage + delta
    else:
        raise Http404

    startdate = datetime.datetime.combine(datepage, datetime.time(00, 00, 01))
    enddate = datetime.datetime.combine(datepage, datetime.time(23, 59, 59))

    startdate = startdate.replace(tzinfo=utcTZ)
    enddate = enddate.replace(tzinfo=utcTZ)

    seances = Seance.objects.select_related().filter(date_debut__gt=startdate, date_fin__lt=enddate).order_by(
        'cinema__nom', 'film__titre', 'date_debut')
    evenements = Evenement.objects.select_related().filter(fin__gt=startdate, debut__lt=enddate, publish=True).order_by(
        'debut')

    equipements_qst = Equipement.objects.all().select_related().order_by('fonction', 'ville__nom', 'nom')
    #   equipement_dict = dict([obj.id,obj] for obj in equipements_qst)
    listhoraires = list()
    #    equipements = list()
    #    for equipement in equipements_qst:
    #            periodes = Periode.objects.filter(date_debut__lte=datepage , date_fin__gte=datepage).filter(horaires__equipement=equipement.id).order_by('date_debut')
    #            if len(periodes) >= 1:
    #                periodes.query.group_by = ['periode_id']
    #                periode_active = periodes[len(periodes) - 1]
    #                horaires = Horaires.objects.filter(equipement=equipement.id).filter(periodes__id=periode_active.id).select_related()
    #                listhoraires.append(horaires)
    #                if equipement not in equipements:
    #                    equipements.append(equipement_dict[equipement.id])


    for equipement in equipements_qst:
        periodes = Periode.objects.filter(date_debut__lte=datepage, date_fin__gte=datepage).filter(
            horaires__equipement=equipement.id).order_by('date_debut')
        if len(periodes) >= 1:
            periodes.query.group_by = ['periode_id']
            periode_active = periodes[len(periodes) - 1]
            horaires = Horaires.objects.select_related().filter(equipement=equipement.id).filter(
                periodes__id=periode_active.id)
            listhoraires.append(horaires)

    numjour = datepage.isoweekday()
    equipements_ouverts = list()
    for horaires in listhoraires:
        for horaire in horaires:
            myJour = horaire.GetDay(numjour)
            if myJour.matin_ferme and myJour.am_ferme:
                continue
            else:
                if horaire.equipement not in equipements_ouverts:
                    equipements_ouverts.append(horaire.equipement)

    # pagination
    suivant_date = datepage + datetime.timedelta(days=1)
    suivant = datetime.datetime.strftime(suivant_date, "%d-%m-%Y")
    precedent_date = datepage + datetime.timedelta(days=-1)
    precedent = datetime.datetime.strftime(precedent_date, "%d-%m-%Y")
    delta = datepage - date.today()
    if delta.days > 8:
        suivant = None
    if delta.days <= 0:
        precedent = None

    return render_to_response('editorial/ephemeride.html',
                              {'datepage': datepage, 'num_jour': datepage.isoweekday(), 'seances': seances,
                               'evenements': evenements, 'equipements': equipements_ouverts,
                               'listhoraires': listhoraires, 'suivant_date': suivant_date,
                               'precedent_date': precedent_date, 'suivant': suivant, 'precedent': precedent})


def newsletterbiblist(request):
    bibliotheques = Equipement.objects.all().filter(type='bib')
    return render_to_response('editorial/newsletters/liste-newsletter.html', {'equipements': bibliotheques})


def newsletterbibhtml(request, equipement_slug):
    bib = Equipement.objects.get(slug=equipement_slug)
    newsletter = NewsletterBib.objects.all().filter(bib=bib).order_by('-maj')[0]
    activites_enfants = Evenement.objects.all().filter(categorie='bib', public='enf', lieu=bib,
                                                       debut__gte=newsletter.evenement_debut,
                                                       fin__lte=newsletter.evenement_fin,
                                                       ).order_by('debut')
    activites_adultes = Evenement.objects.all().filter(categorie='bib', public='adt', lieu=bib,
                                                       debut__gte=newsletter.evenement_debut,
                                                       fin__lte=newsletter.evenement_fin).order_by('debut')
    activites_ttpublic = Evenement.objects.all().filter(categorie='bib', public='pub', lieu=bib,
                                                        debut__gte=newsletter.evenement_debut,
                                                        fin__lte=newsletter.evenement_fin).order_by('debut')

    return render_to_response('editorial/newsletters/newsletter.html', {'bib': bib,
                                                                        'request': request,
                                                                        'activites_enfants': activites_enfants,
                                                                        'activites_adultes': activites_adultes,
                                                                        'activites_ttpublic': activites_ttpublic,
                                                                        'edito': newsletter.edito
                                                                        })

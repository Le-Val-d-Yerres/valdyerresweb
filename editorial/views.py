# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response , redirect , get_object_or_404
from editorial.models import Magazine
from cinemas.models import Seance
from evenements.models import Evenement
from equipements.models import Equipement
from horaires.models import Horaires, Periode
from pytz import timezone, tzinfo
from datetime import date
from valdyerresweb import settings
import datetime


myTZ = timezone(settings.TIME_ZONE)
utcTZ = timezone("UTC")


def Home(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

def ActuLists(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

def ActuDetail(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})


def PageDetail(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

def Magazines(request):
    
    magazines_list = Magazine.objects.filter(publie=True).order_by('-date_parution')
    paginator = Paginator(magazines_list,5)
    page = request.GET.get('page')
    
    try:
        if page == None:
            magazines = paginator.page(1)
        elif page =="":
            return redirect('magazines')
        elif int(page) == 1:
            return redirect('magazines')
        else:
            magazines = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404

    return render_to_response('editorial/magazines.html',{'magazines' : magazines})



def Ephemeride(request,jour):
    jourdate = jour.split('-')
    datepage = date.today()
    if len(jourdate) == 3:
        tmpdate = datetime.datetime.strptime(jour,"%d-%m-%Y").date()
        if tmpdate == datepage:
            redirect('ephemeride','aujourd-hui')
        
    elif jour == "aujourd-hui":
        datepage = date.today()
    elif jour == "demain":
        delta = datetime.timedelta(days=1)
        datepage = datepage +delta
    else:
        raise Http404
        

        
    startdate = datetime.datetime.combine(datepage,datetime.time(00, 00, 01))
    enddate = datetime.datetime.combine(datepage,datetime.time(23, 59, 59))
    
    startdate = startdate.replace(tzinfo=utcTZ)
    enddate = enddate.replace(tzinfo=utcTZ)
    
    seances = Seance.objects.select_related().filter(date_debut__gt = startdate, date_fin__lt = enddate).order_by('cinema__nom','film__titre','date_debut')
    
    evenements = Evenement.objects.select_related().filter(fin__gt=startdate,debut__lt = enddate, publish = True).order_by('debut')
    
    equipements_qst = Equipement.objects.all().select_related().order_by('fonction','ville__nom','nom')
    equipement_dict = dict([obj.id,obj] for obj in equipements_qst)
    
    listhoraires = list()
    equipements = list()
    
    for equipement in equipements_qst:
            periodes = Periode.objects.filter(date_debut__lte=datepage , date_fin__gte=datepage).filter(horaires__equipement=equipement.id).order_by('date_debut')
            if len(periodes) >= 1:
                periodes.query.group_by = ['periode_id']
                periode_active = periodes[len(periodes) - 1]
                horaires = Horaires.objects.filter(equipement=equipement.id).filter(periodes__id=periode_active.id).select_related()
                listhoraires.append(horaires)
                if equipement not in equipements:
                    equipements.append(equipement_dict[equipement.id])

    
    
    return render_to_response('editorial/ephemeride.html',{'datepage':datepage,'num_jour':datepage.isoweekday(),'seances' : seances,'evenements':evenements, 'equipements': equipements , 'listhoraires':listhoraires })
    
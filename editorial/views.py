# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response , redirect , get_object_or_404
from editorial.models import Magazine
from cinemas.models import Seance
import datetime
from datetime import date

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
    
    datepage = date.today()
    if jour == "aujourd-hui":
        datepage = date.today()
    if jour == "demain":
        delta = datetime.timedelta(days=1)
        datepage = datepage +delta
        
    startdate = datetime.datetime.combine(datepage,datetime.time(00, 00, 01))
    enddate = datetime.datetime.combine(datepage,datetime.time(23, 59, 59))
    seances = Seance.objects.select_related().filter(date_debut__gt = startdate, date_fin__lt = enddate).order_by('cinema__nom','film__titre','date_debut')
    
    return render_to_response('editorial/ephemeride.html',{'datepage':datepage,'seances' : seances})
    
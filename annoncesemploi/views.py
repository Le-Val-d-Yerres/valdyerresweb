# -*- coding: utf-8 -*-
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response , redirect , get_object_or_404,\
    get_list_or_404

from models import Annonce    
from valdyerresweb import settings
from pytz import timezone, tzinfo
from services.models import Service


myTZ = timezone(settings.TIME_ZONE)
utcTZ = timezone("UTC")

def AnnoncesList(request):
    
    annonces =  Annonce.objects.filter(publie=True).order_by('service')
    
    paginator = Paginator(annonces,5)
    
    page = request.GET.get('page')

    
    try:
        if page == None:
            pages = paginator.page(1)
        elif page =="":
            return redirect('annonces-list')
        elif int(page) == 1:
            return redirect('annonces-list')
        else:
            pages = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404
    
    return render_to_response('annoncesemploi/annonces-list.html', {'pages' : pages})

def AnnoncesListService(request, service_slug):
    service = get_object_or_404(Service,slug=service_slug)
    annonces =  Annonce.objects.filter(publie=True,service__slug=service.slug).order_by('intitule')
    message = None
    if len(annonces) == 0:
        message = "Désolé, ce service ne propose pas d'annonces pour le moment"
        
    
    paginator = Paginator(annonces,5)
    
    page = request.GET.get('page')

    try:
        if page == None:
            pages = paginator.page(1)
        elif page =="":
            return redirect('annonces-list')
        elif int(page) == 1:
            return redirect('annonces-list')
        else:
            pages = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        raise Http404    
    
    return render_to_response('annoncesemploi/annonces-list.html', {'pages' : pages, 'message':message})


def AnnonceDetail(request,annonce_slug):
    annonce = get_object_or_404(Annonce.objects.select_related(),slug = annonce_slug, publie=True)
    return render_to_response('annoncesemploi/annonce.html', {'annonce':annonce})
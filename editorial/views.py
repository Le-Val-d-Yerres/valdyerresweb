# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , redirect , get_object_or_404
from editorial.models import Magazine


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
    magazines = Magazine.objects.filter(publie=True).order_by('-date_parution')
    return render_to_response('editorial/magazines.html',{'magazines' : magazines})
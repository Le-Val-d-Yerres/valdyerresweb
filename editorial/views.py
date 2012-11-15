# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , redirect , get_object_or_404



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
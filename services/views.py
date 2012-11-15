
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , redirect , get_object_or_404



def ListeServices(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

def ServiceDetail(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

def PageContenu(request):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

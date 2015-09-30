# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from forms import FicheForm
from models import Fichestagecrd, Stage, Disciplinestagecrd, Intitulestage
from django.forms.models import inlineformset_factory

# Create your views here.

def formfichestage(request):

    if request.method == "POST":
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        choix_1 = request.POST['choix_1']
        choix_2 = request.POST['choix_2']
        choix_3 = request.POST['choix_3']
        commentaire = request.POST['commentaire']
        
        return HttpResponseRedirect('merci.html')


    params = {}
    intitules = Intitulestage.objects.all()
    params.update({'intitules': intitules})
    disciplines = Disciplinestagecrd.objects.all()
    params.update({'disciplines': disciplines})


    return render_to_response('forms/fichestageform.html', params)

def merci(request):
    return render_to_response('forms/merci.html')
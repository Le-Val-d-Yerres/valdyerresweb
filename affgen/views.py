# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import QualifMandat,Elu, Cptrendu
from collections import namedtuple

from django.shortcuts import render_to_response, redirect, get_object_or_404, \
    get_list_or_404


def homeaffgen(request):
    return redirect('home')


def elus(request):
    mandats = QualifMandat.objects.all().order_by('index')
    elusst = list()
    elusnd = list()

    MandatTuple = namedtuple('MandatTuple','mandat listeelus')

    for mandat in mandats[:3]:

        elustmp = list()
        leselus =Elu.objects.filter(publie=True, mandatagglo__qualif_id=mandat.id).order_by('mandatagglo__index').select_related()
        for elu in leselus:
            elustmp.append(elu)

        mandatagglo = MandatTuple(mandat, elustmp)
        elusst.append(mandatagglo)


    for mandat in mandats[3:]:
        leselus = Elu.objects.filter(publie=True, mandatagglo__qualif_id=mandat.id).order_by(
            'ville','mandatagglo__index').select_related()
        for elu in leselus:
            elusnd.append(elu)


    return render_to_response('liste_elus.html', {'elusst': elusst, 'elusnd':elusnd})


def comptesrendus(request):
    cptrd = Cptrendu.objects.all().order_by('-date')
    return render_to_response('comptes_rendus.html', {'cptrd': cptrd})

def compterendu(request, idcpt):
    cptrendu = get_object_or_404(Cptrendu, date=idcpt)
    return render_to_response('compte_rendu.html', {'cptrendu': cptrendu})
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response , redirect , get_object_or_404
from .models import Entreprise, Dirigeant
from valdyerresweb.utils.functions import GenerationQrCode
from django.template import loader
from django.http import Http404, HttpResponse


def home(request):
    entreprises = Entreprise.objects.filter(publie=True).order_by('nom')

    params = {}
    params.update({"entreprises": entreprises})
    return render_to_response("deveco/home.html", params)


def entreprise(request, slug):
    params = {}
    monentreprise = get_object_or_404(Entreprise, slug=slug, publie=True)
    params.update({"entreprise": monentreprise})
    dirigeants = Dirigeant.objects.filter(entreprise=monentreprise)
    params.update({"dirigeants": dirigeants})
    qr_code_geo = GenerationQrCode("geo:" + str(monentreprise.latitude) + "," + str(monentreprise.longitude))
    params.update({"qr_code_geo": qr_code_geo})
    qr_code_vcard = GenerationQrCode(genentreprisevcard(monentreprise.slug))
    params.update({"qr_code_vcard": qr_code_vcard})
    return render_to_response("deveco/entreprise.html", params)


def genentreprisevcard(slug):
    monentreprise = get_object_or_404(Entreprise, slug=slug)
    mycontext = {"entreprise": monentreprise}
    mytemplate = loader.get_template('deveco/entreprise.vcard.html')
    return mytemplate.render(mycontext)


def entreprisevcard(request, slug):
    vcard = genentreprisevcard(slug)
    return HttpResponse(vcard, content_type="text/vcard")


def home3(request):
    params = {}
    return render_to_response("deveco/home.html", params)
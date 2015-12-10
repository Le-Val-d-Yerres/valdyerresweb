from django.shortcuts import render_to_response , redirect , get_object_or_404
from models import Entreprise
from valdyerresweb.utils.functions import GenerationQrCode
from django.template import Context, loader


def home(request):
    entreprises = Entreprise.objects.filter(publie=True).order_by('nom')

    params = {}
    params.update({"entreprises": entreprises})
    return render_to_response("deveco/home.html", params)


def entreprise(request, slug):
    monentreprise = get_object_or_404(Entreprise, slug=slug)
    qr_code_geo = GenerationQrCode("geo:" + str(monentreprise.latitude) + "," + str(monentreprise.longitude))
    qr_code_vcard = GenerationQrCode(genentreprisevcard(monentreprise.slug))
    params = {}
    params.update({"entreprise": monentreprise})
    params.update({"qr_code_geo": qr_code_geo})
    params.update({"qr_code_vcard": qr_code_vcard})
    return render_to_response("deveco/entreprise.html", params)


def genentreprisevcard(slug):
    monentreprise = get_object_or_404(Entreprise, slug=slug)
    params = {}
    params.update({"entreprise": monentreprise})
    mytemplate = loader.get_template('deveco/entreprise.vcard.html')
    return mytemplate.render(params)


def entreprisevcard(request, slug):
    monentreprise = get_object_or_404(Entreprise, slug=slug)
    params = {}
    params.update({"entreprise": monentreprise})
    mytemplate = loader.get_template('deveco/entreprise.vcard.html')
    return mytemplate.render(params)


def home3(request):
    params = {}
    return render_to_response("deveco/home.html", params)
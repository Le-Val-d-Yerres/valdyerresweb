from django.shortcuts import render_to_response , redirect , get_object_or_404
from models import Entreprise


def home(request):
    entreprises = Entreprise.objects.filter(publie=True).order_by('nom')

    params = {}
    params.update({"entreprises": entreprises})
    return render_to_response("deveco/home.html", params)


def entreprise(request, slug):
    monentreprise = get_object_or_404(Entreprise,slug=slug)
    params = {}
    params.update({"entreprise": monentreprise})
    return render_to_response("deveco/home.html", params)


def home3(request):
    params = {}
    return render_to_response("deveco/home.html", params)
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .models import FicheInscription
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import FicheInscription

# Create your views here.


def formficheinscription(request):
    if request.method == "POST":
        fiche = FicheInscription
        fiche.nom = request.POST["nom"]
        fiche.prenom = request.POST["prenom"]
        fiche.datenaissance = request.POST["datenaissance"]
        fiche.sexe = request.POST["sexe"]
        fiche.email = request.POST["email"]
        fiche.adresse = request.POST["adresse"]
        fiche.code_postal = request.POST["codepostal"]
        fiche.ville = request.POST["ville"]
        fiche.save()

    params = {}


    return render_to_response('formficheinscription.html', params)

def merci(request):
    return render_to_response('merci.html')
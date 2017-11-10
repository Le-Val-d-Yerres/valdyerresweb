from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .models import FicheInscription
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import FicheInscription
import time

# Create your views here.


def formficheinscription(request):
    message = None
    if request.method == "POST":
        fiche = FicheInscription()
        fiche.nom = request.POST["nom"]
        fiche.prenom = request.POST["prenom"]
        datenaissance = request.POST["datenaissance"]
        datenaissance = datenaissance.split('/')
        datenaissance = datenaissance[2]+'-'+datenaissance[1]+'-'+datenaissance[0]
        fiche.datenaissance = datenaissance
        fiche.sexe = request.POST["sexe"]
        fiche.email = request.POST["email"]
        fiche.adresse = request.POST["adresse"]
        fiche.code_postal = request.POST["codepostal"]
        fiche.ville = request.POST["ville"]
        fiche.telephone = request.POST["telephone"]
        fiche.profession = request.POST["profession"]
        fiche.save()
        mydatenaissance = time.strptime(datenaissance, "%d-%m-%Y")
        print(mydatenaissance)


    params = {'message': message}
    return render_to_response('formficheinscription.html', params)

def merci(request):
    return render_to_response('merci.html')
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import FicheInscription
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import FicheInscription
import datetime

# Create your views here.

def check18y(datenaiss):
    tabdate = datenaiss.split("-")
    year = int(tabdate[0])
    month = int(tabdate[1])
    day = int(tabdate[2])
    if month == 2 and day == 29:
        month = 2
        day = 28

    mydate = datetime.date(year=year, month=month, day=day)
    today = datetime.date.today()
    datecheck = None
    if mydate.year > ((today.year - 18)):
        return True
    if mydate.year <= (today.year - 18):
        datecheck = datetime.date(today.year-12 ,month=month, day=day)
        if (today - datecheck) >= 0:
            return True
        else:
            return False





def formficheinscription(request):
    message18y = False
    message18ybis = False
    if request.method == "POST":
        mineurid = request.POST["mineurid"]
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



        if check18y(datenaissance) is False:
            if mineurid:
                message18y = False
                message18ybis = True
                params = {'message18y' : message18y, 'message18ybis': message18ybis, 'mineurid': mineurid}
            else:
                fiche.save()
                message18y = True
                message18ybis = False
                params = {'message18y': message18y, 'message18ybis': message18ybis, 'mineurid':fiche.uuid}
            return render_to_response('formficheinscription.html', params)

        if mineurid:
            fichemineur = get_object_or_404(FicheInscription, uuid=mineurid)
            fiche.adultereferent_id = fichemineur.id
            fiche.save()



    message18y = False
    message18ybis = False
    params = {'message18y': message18y, 'message18ybis': message18ybis, 'mineurid': None}
    return render_to_response('formficheinscription.html', params)



def merci(request):
    return render_to_response('merci.html')
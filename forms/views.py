# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import Fichestagecrd, Stage, Disciplinestagecrd, Intitulestage
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from random import random
from django.forms.models import inlineformset_factory
import csv
from StringIO import StringIO

vacances = ["toussaint_1", "toussaint_2", "hiver_1", "hiver_2", "paques_1", "paques_2", "ete_1", "ete_2"]

# Create your views here.

def formfichestage(request):

    if request.method == "POST":
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        choix_1 = request.POST['choix_1']
        choix_2 = request.POST['choix_2']
        choix_3 = request.POST['choix_3']
        commentaire = request.POST['commentaire']
        fiche = Fichestagecrd()
        fiche.nom = nom
        fiche.prenom = prenom
        fiche.choix_1 = Disciplinestagecrd.objects.get(id=choix_1)
        fiche.choix_2 = Disciplinestagecrd.objects.get(id=choix_2)
        fiche.choix_3 = Disciplinestagecrd.objects.get(id=choix_3)
        fiche.commentaires = commentaire
        fiche.save()

        intitules = Intitulestage.objects.all()
        for intitule in intitules:
            for i in range(1, 9):
                try:
                    monintitule = request.POST["stage_"+str(intitule.id)+"-"+str(i)]
                    monintitule = monintitule.split("-")[0]
                    print(monintitule)
                except Exception:
                    continue
                try:
                    monstage = Stage.objects.get(fiche=fiche, intitule=intitule)
                except Stage.DoesNotExist:
                    monstage = Stage()
                    monstage.intitule = intitule
                    monstage.fiche = fiche

                setattr(monstage, monintitule, True)

                monstage.save()

        return HttpResponseRedirect('merci.html')

    params = {}
    intitules = Intitulestage.objects.all()
    params.update({'intitules': intitules})
    disciplines = Disciplinestagecrd.objects.all()
    params.update({'disciplines': disciplines})
    return render_to_response('forms/fichestageform.html', params)


def merci(request):
    return render_to_response('forms/merci.html')

@never_cache
@login_required(login_url='/admin/login/')
def exportcrd(request):
    myfile = StringIO()
    file_type = 'application/csv'
    file_name = 'export.csv'
    mycsv = csv.writer(myfile, delimiter=';', quotechar='"')
    intitules = Intitulestage.objects.all().order_by('index')
    stagesnom = tuple(intitule.nom.encode('UTF-8') for intitule in intitules)
    headers = (u"nom", u"prenom", u'commentaire', u"choix 1", u"choix 2", u"choix 3")
    headers = headers+stagesnom
    mycsv.writerow(headers)
    fiches = Fichestagecrd.objects.all().order_by('nom', 'prenom')
    for fiche in fiches:
        myrow = (fiche.nom.encode('UTF-8'), fiche.prenom.encode('UTF-8'), fiche.commentaires.encode('UTF-8'), fiche.choix_1.nom.encode('UTF-8'), fiche.choix_2.nom.encode('UTF-8'), fiche.choix_3.nom.encode('UTF-8'))
        myrowpar2 = tuple()
        for intitule in intitules:
            myvalue = ""
            nbstage = Stage.objects.all().filter(fiche=fiche, intitule=intitule).count()
            if nbstage is 1:
                stage = Stage.objects.get(fiche=fiche, intitule=intitule)
                check = False
                for key in vacances:
                    if getattr(stage, key) is True:
                        check = True
                        myvalue = myvalue + key + " "
                        myrowpar2 = myrowpar2 +(myvalue,)
                if check is False:
                        myrowpar2 = myrowpar2 + ("na",)
            if nbstage is 0:
                myrowpar2 = myrowpar2 + ("na",)



        mycsv.writerow(myrow+myrowpar2)

    myfile.seek(0)
    response = HttpResponse(myfile.read(), content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename='+file_name
    response['Content-Length'] = myfile.tell()
    return response

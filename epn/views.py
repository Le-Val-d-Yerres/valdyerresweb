from uuid import uuid4
import datetime
import io
import cairosvg
import csv

from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from .models import FicheInscription
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import FicheInscription



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
    if mydate.year >= (today.year - 18):
        datecheck = datetime.date(today.year-18, month=month, day=day)
        if (mydate.year == datecheck.year) and ((today - datecheck).days >= 0):
            return True
        else:
            return False
    if mydate.year < (today.year - 18):
        return True






def formficheinscription(request):
    message18y = False
    message18ybis = False
    mineurid = None
    fichemineur = None
    fiche = None

    if request.method == "POST":
        try:
            mineurid = request.POST["mineurid"]
        except Exception:
            mineurid = None

        fiche = FicheInscription()
        fiche.uuid = str(uuid4())
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
        fiche.dateinscription = datetime.datetime.now()

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

        fiche.save()

        if mineurid:
            fichemineur = get_object_or_404(FicheInscription, uuid=mineurid)
            fichemineur.adultereferent_id = fiche.id
            fichemineur.save()



        message18y = False
        message18ybis = False
        params = {'message18y': message18y, 'message18ybis': message18ybis, 'mineurid': None}
        if fichemineur:
            fiche = fichemineur

        return redirect('inscription', fiche.uuid)

    params = {'message18y' : message18y, 'message18ybis': message18ybis, 'mineurid': mineurid}
    return render_to_response('formficheinscription.html', params)


def inscription(request, uuid):
    fiche = get_object_or_404(FicheInscription, uuid=uuid)
    params = {'fiche': fiche}
    return render_to_response('inscription.html', params)



def getpdf(request, uuid):
    fiche = get_object_or_404(FicheInscription, uuid=uuid)
    ficheadulte = None
    svg = None
    params = {'fiche': fiche}


    if fiche.adultereferent_id:
        ficheadulte = get_object_or_404(FicheInscription,id=fiche.adultereferent_id)
        params = {'fiche': fiche, 'ficheadulte': ficheadulte}
        svg = render_to_string('fiche-mineur.svg', params)
    else:
        svg = render_to_string('fiche-new.svg', params)

    buffer = io.BytesIO()
    buffer.write(cairosvg.svg2pdf(svg))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fiche-inscription.pdf"'
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


@never_cache
@login_required(login_url='/admin/login/')
def exportepn(request):
    myfile = io.StringIO()
    file_type = 'application/csv'
    file_name = 'export.csv'
    mycsv = csv.writer(myfile, delimiter=';', quotechar='"')
    fiches = FicheInscription.objects.all().order_by('dateinscription')
    headers = (u"id",u"nom", u"prenom", u'date de naissance', u"sexe", u"email", u"adresse",u"code postal", u"ville", u"profession", u'telephone', u'referent',u'numero adherent')
    mycsv.writerow(headers)
    for fiche in fiches:
        row = (fiche.id,fiche.nom, fiche.prenom, fiche.datenaissance, fiche.sexe, fiche.email, fiche.adresse, fiche.code_postal, fiche.ville, fiche.profession, fiche.telephone, fiche.adultereferent_id, fiche.numero_adherent)
        mycsv.writerow(row)

    myfile.seek(0)
    response = HttpResponse(myfile.read(), content_type=file_type)
    response['Content-Disposition'] = 'attachment; filename='+file_name
    response['Content-Length'] = myfile.tell()
    return response
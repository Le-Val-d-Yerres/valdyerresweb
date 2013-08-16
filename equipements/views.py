# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response , redirect , get_object_or_404, get_list_or_404
from equipements.models import Equipement,EquipementFonction,TarifCategorie,Tarif , Facilites, Facilite, AlertesReponses, Alerte
from evenements.models import Evenement, Organisateur
from localisations.models import Lieu
from horaires.models import Horaires, Periode
import datetime
from django.db.models import Q
from django.conf import settings
from pytz import timezone
from django.template import Context, loader
from valdyerresweb.utils.functions import GenerationQrCode, validateEmail
from valdyerresweb.templatetags import filtres
import uuid
import re


utcTZ = timezone("UTC")

def EquipementsCarte(request):
      
    equipements = Equipement.objects.select_related().all().order_by('fonction__nom', 'ville__nom')

    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'mediaDir': settings.MEDIA_DIR_NAME})

def FaciliteCarte(request,slug):
    
    facilite = get_object_or_404(Facilite.objects.filter(slug=slug))
    
    facilites = Facilites.objects.prefetch_related().select_related().filter(facilites=facilite.id)
    
    
    
    dict_lieux = {}
    lieux = Lieu.objects.all().select_related().select_subclasses()
    for lieu in lieux:
        dict_lieux[lieu.id] = lieu
    
    
    list_facilites = list()
    
    
    
    for item in facilites:
        item.equipement = dict_lieux[item.equipement.id]
        list_facilites.append(item)

    
    return render_to_response('equipements/carte-facilites.html', {'lieux':lieux,'facilite': facilite,'facilites': list_facilites, 'mediaDir': settings.MEDIA_DIR_NAME})

def FaciliteListe(request):
    equipements = Equipement.objects.select_related().all()
    facilites = Facilites.objects.select_related().all()
    facilite_geo = Facilite.objects.filter(importance__lt = 10)
    
    dict_equipements = {}
    for equipement in equipements:
        dict_equipements[equipement.id]=equipement
    
    list_facilites = list()
    for item in facilites:
        item.equipement = dict_equipements[item.equipement.pk]
        list_facilites.append(item)
    
    list_facilites = reversed(sorted(list_facilites, key= lambda facilite: facilite.equipement.fonction.id ))
    
    return render_to_response('equipements/facilites.html',{'facilites':list_facilites,'facilite_geo':facilite_geo})

def EquipementsDetailsHtml(request, fonction_slug, equipement_slug):

    now = datetime.datetime.now(utcTZ)
    equipement = get_object_or_404(Equipement.objects.select_related().filter(fonction__slug=fonction_slug), slug=equipement_slug)
    
    tarif_categorie_principale = TarifCategorie.objects.select_related().filter(equipement_fonction = equipement.fonction,index=0 ) 
    tarifs_principaux = Tarif.objects.select_related().filter(categorie= tarif_categorie_principale )
        
    facilites = Facilites.objects.filter(equipement_id=equipement.id)
    
    evenements = None
    try:
        organisateur = Organisateur.objects.get(orga_equipement = equipement.id)
        evenements = Evenement.objects.select_related().filter(Q(organisateur = organisateur.id) | Q(lieu_id=equipement.id) , fin__gt=now , publish=True).order_by('debut')
    except Organisateur.DoesNotExist:
        evenements = Evenement.objects.select_related().filter(lieu_id=equipement.id , fin__gt=now , publish=True).order_by('debut')
        
    
    #<trash>
    try:
        facilites = facilites[0]
    except:
        facilites = None
    #</trash>
        
    today = datetime.date.today()
    horaires = None
    periodes = Periode.objects.filter(date_debut__lte=today , date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    if len(periodes) >= 1:
        periode_active = periodes[len(periodes) - 1]
        horaires = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active.id)
    else:
        periode_active = None
        
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    horaires_demain = None
    periodes_demain = Periode.objects.filter(date_debut__lte=tomorrow , date_fin__gte=tomorrow).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes_demain.query.group_by = ['periode_id']
    if len(periodes_demain) >= 1:
        periode_active_demain = periodes[len(periodes) - 1]
        horaires_demain = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active_demain.id)
    else:
        periode_active_demain = None
        
        
    autres_periodes = Periode.objects.filter(date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    autres_periodes.query.group_by = ['periode_id']
    
    horaires_plus_7 = list()
    
    for index in range(1,8):
        day = datetime.date.today() + datetime.timedelta(days=index)
        horaires_jour = None
        periodes_jour = Periode.objects.filter(date_debut__lte=day , date_fin__gte=day).filter(horaires__equipement=equipement.id).order_by('date_debut')
        periodes_jour.query.group_by = ['periode_id']
        if len(periodes_jour) >= 1:
            periode_active_jour = periodes_jour[len(periodes_jour) - 1]
            horaires_jour = Horaires.objects.filter(equipement=equipement.id).filter(periodes__id=periode_active_jour.id)
            horaires_plus_7.append(horaires_jour)
        else:
            periode_active_jour = None
         
    qr_code_geo = GenerationQrCode("geo:" + str(equipement.latitude) + "," + str(equipement.longitude))
    qr_code_vcard = GenerationQrCode(EquipementVcard(equipement))
    
    tokenCSRF = uuid.uuid1()
    
    alerte = {
        'nom': 'Signaler un problème',
        'cible': '<img src="'+filtres.resize(equipement.image, '100x100x1')+'" style="float:left;margin-right: 10px;" class="img-polaroid"><address style="width: 500px;"><strong>'+equipement.nom+'</strong><br \>'+equipement.rue+'<br \>'+equipement.ville.code_postal+' '+equipement.ville.nom+'<br \>'+equipement.telephone+'</address>',
        'id': 2,
        'token': tokenCSRF,
        'equipement': 15
    }
        
    reponse = render_to_response('equipements/equipement-details.html', {'alerte': alerte, 'equipement': equipement, 'qr_code_geo': qr_code_geo, 'qr_code_vcard': qr_code_vcard, 'facilites': facilites, 'evenements': evenements, 'horaires':horaires, 'periode_active':periode_active, 'autres_periodes':autres_periodes, 'horaires_demain':horaires_demain, 'periode_active_demain':periode_active_demain , 'horaires_plus_7': horaires_plus_7, 'tarifs_principaux':tarifs_principaux })
    reponse.set_cookie("csrftoken", tokenCSRF, 60*5)
    
    return reponse

def EquipementHoraires(request, equipement_slug):
    equipement = get_object_or_404(Equipement.objects.select_related() , slug=equipement_slug)
    today = datetime.date.today()
    periodes = Periode.objects.filter(date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    horaires = Horaires.objects.prefetch_related('periodes').select_related().filter(equipement=equipement.id)
    for periode in periodes:
        horaires.filter(periodes__id = periode.id)
    
    if len(horaires) == 0:
        raise Http404
    
    
    return render_to_response('equipements/equipement-horaires.html', {'equipement':equipement,'horaires':horaires, 'periodes':periodes})


def EquipementFonctionTarifs(request, equipement_fonction_slug):
    fonction = get_object_or_404(EquipementFonction.objects, slug=equipement_fonction_slug)
    tarifs = Tarif.objects.select_related().filter(categorie__equipement_fonction__slug = equipement_fonction_slug)
    equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id).order_by('ville__nom')
            
    return render_to_response('equipements/equipement-tarifs.html', {'tarifs':tarifs,'equipements':equipements})
    


def FonctionDetailsHtml(request, fonction_slug):
    fonction = get_object_or_404(EquipementFonction.objects, slug=fonction_slug)
    equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id).order_by('ville__nom')
        
    today = datetime.date.today()
    listhoraires = list()
    
    for equipement in equipements:
        periodes = Periode.objects.filter(date_debut__lte=today , date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
        if len(periodes) >= 1:
            periodes.query.group_by = ['periode_id']
            periode_active = periodes[len(periodes) - 1]
            horaires = Horaires.objects.select_related().filter(equipement=equipement.id).filter(periodes__id=periode_active.id)
            listhoraires.append(horaires)

    return render_to_response('equipements/carte-fonction-equipements.html', {'equipements': equipements, 'fonction': fonction, 'listhoraires': listhoraires})

def EquipementVCF(request, slug):
    lieu = get_object_or_404(Lieu.objects.select_related().select_subclasses(), slug=slug)
    
    myText = EquipementVcard(lieu)

    return HttpResponse(myText, content_type="text/vcard")

def EquipementVcard(equipement):
    myTemplate = loader.get_template('equipements/equipement.vcf.html')
    myContext = Context({"equipement": equipement, "settings": settings})
    return myTemplate.render(myContext)

def EquipementTarifs(request):
    tarifs = Tarif.objects.select_related().order_by('categorie__equipement_fonction__nom').filter(categorie__index=0)
    
    listeEquipements = []
    
    for each in tarifs:
        if each.categorie.equipement_fonction not in listeEquipements:
            listeEquipements.append(each.categorie.equipement_fonction)
            
    if len(listeEquipements) == 0:
            raise Http404
        
    return render_to_response('equipements/equipement-tarifs-complet.html', {'tarifs':tarifs, 'listeEquipements':listeEquipements})

def HorairesTousEquipements(request):
    horaires = Horaires.objects.all()
    
    listeEquipements = []
    
    for each in horaires:
        if each.equipement not in listeEquipements:
            listeEquipements.append(each.equipement)

    if len(listeEquipements) == 0:
            raise Http404
    
    for each in listeEquipements:
        equipement = get_object_or_404(Equipement.objects.select_related() , slug=each.slug)
        today = datetime.date.today()
        periodes = Periode.objects.filter(date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
        periodes.query.group_by = ['periode_id']
        each.periodes = periodes
        horaires = Horaires.objects.prefetch_related('periodes').select_related().filter(equipement=equipement.id)
        for periode in periodes:
            horaires.filter(periodes__id = periode.id)
        
        each.periodes.horaires = horaires
        
    return render_to_response('equipements/tous-equipement-horaires.html', {'listeEquipements':listeEquipements})

def AlertesAjax(request):
    
    result = re.match('^[0-9 ]+$', request.POST['tel'])
    longueur = len(request.POST['tel'])
    if result and (longueur == 10 or longueur == 14):     
        if validateEmail(request.POST['mail']):
            alerte = AlertesReponses()
            alerte.nom = request.POST['nom']
            alerte.prenom = request.POST['prenom']
            alerte.rue = request.POST['rue']
            alerte.codePostal = request.POST['codePostal']
            alerte.ville = request.POST['ville']
            alerte.tel = request.POST['tel']
            alerte.mail = request.POST['mail']
            alerte.message = request.POST['msg']
            alerte.ip = request.META.get('REMOTE_ADDR')
            alerte.etat = False
            alerte.date = datetime.datetime.now(utcTZ)
            
            alerteTemplate = Alerte.objects.filter(id=request.POST['alerteId'])
    
            equipement = Equipement.objects.filter(id=request.POST['equipementId'])
            
            if len(alerteTemplate) == 0 or len(equipement) == 0:
                return HttpResponse("2", content_type="text/plain")
            else:
                alerteTemplate = Alerte.objects.filter(id=request.POST['alerteId'])[0]
    
                equipement = Equipement.objects.filter(id=request.POST['equipementId'])[0]
            
                alerte.equipement = equipement
                alerte.alerte = alerteTemplate
            
            alerte.save()
            
            return HttpResponse("1", content_type="text/plain")
        else:
            # Adresse mail non valide
            return HttpResponse("0", content_type="text/plain")
    else:
            # tel non valide
            return HttpResponse("3", content_type="text/plain")

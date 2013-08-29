# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response , redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from valdyerresweb import settings
from lettreinformations import settings as conf
from django.template import Context,loader
from django.core.cache import cache
from lettreinformations.utils import mailjet
from valdyerresweb.utils import functions
from django.template import RequestContext
import uuid
from django.views.decorators.cache import never_cache

@never_cache
def mailForm(request):
    tokenCSRF = uuid.uuid1()
    
    reponse = render_to_response('lettreinformations/mail-form.html', {'token':tokenCSRF})
    reponse.set_cookie("csrftoken", tokenCSRF, 60*5)

    return reponse
    
def mailValidation(request, hash):
    if cache.has_key(hash):
        mail = cache.get(hash)
        
        rep = mailjet.addContact(mail, conf.MAIL_LIST_ID)

        if rep == 1 or rep == 3:
            cache.delete(hash)
    else:
        rep = 4

    tokenCSRF = uuid.uuid1()
    
    reponse = render_to_response('lettreinformations/mail-validation-reponse.html', {'reponse': rep, 'token': tokenCSRF})
    reponse.set_cookie("csrftoken", tokenCSRF, 60*5)
    return reponse
            
def mailJetAjax(request):
    if request.COOKIES.has_key('csrftoken'):
        if request.COOKIES['csrftoken'] == request.POST['csrftoken']:
            mail = request.POST['email']
            
            if functions.validateEmail(mail):
                
                rep = mailjet.isContactInList(mail, conf.MAIL_LIST_ID)
                
                if rep == 1:
                    UserUUID = uuid.uuid1()
                    cache.set(UserUUID, mail, 86400)
                    
                    msg = MIMEMultipart('alternative')
                    
                    msg['Subject'] = u"Veuillez confirmer votre abonnement à la lettre d'informations"
                    msg['From'] = 'levaldyerres@levaldyerres.fr'
                    msg['To'] = mail
                    
                    myTemplate = loader.get_template('lettreinformations/mail-validation-html.html')
                    myContext = Context({"hash": UserUUID, "mail": mail, "domaine": settings.NOM_DOMAINE})
                    html = myTemplate.render(myContext)
                    
                    myTemplate = loader.get_template('lettreinformations/mail-validation-txt.html')
                    myContext = Context({"hash": UserUUID, "mail": mail, "domaine": settings.NOM_DOMAINE})
                    text = myTemplate.render(myContext)
                    
                    text = text.encode('utf-8')
                    html = html.encode('utf-8')
                    
                    part1 = MIMEText(text, 'plain', "utf-8")
                    part2 = MIMEText(html, 'html', "utf-8")
                    
                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    msg.attach(part1)
                    msg.attach(part2)
                    
                    reponse = mailjet.envoiMail(mail, msg)
                    
                    return HttpResponse(str(reponse), content_type="text/plain")
                else:
                    return HttpResponse(str(rep), content_type="text/plain")
            else:
                # Adresse non valide
                return HttpResponse("0", content_type="text/plain")
        else:
            return HttpResponse("2", content_type="text/plain")
    else:
        # absence cookie
        return HttpResponse("4", content_type="text/plain")

@never_cache
def mailJetPost(request):
    if request.COOKIES.has_key('csrftoken'):
        if request.COOKIES['csrftoken'] == request.POST['csrftoken']:
            mail = request.POST['email']
            
            if functions.validateEmail(mail):
                UserUUID = uuid.uuid1()
                cache.set(UserUUID, mail, 86400)
                    
                msg = MIMEMultipart('alternative')
                
                msg['Subject'] = u"Veuillez confirmer votre abonnement à la lettre d'informations"
                msg['From'] = 'levaldyerres@levaldyerres.fr'
                msg['To'] = mail
                
                rep = mailjet.isContactInList(mail, conf.MAIL_LIST_ID)
                
                if rep == 1:
                    myTemplate = loader.get_template('lettreinformations/mail-validation-html.html')
                    myContext = Context({"hash": UserUUID, "mail": mail, "domaine": settings.NOM_DOMAINE})
                    html = myTemplate.render(myContext)
                    
                    myTemplate = loader.get_template('lettreinformations/mail-validation-txt.html')
                    myContext = Context({"hash": UserUUID, "mail": mail, "domaine": settings.NOM_DOMAINE})
                    text = myTemplate.render(myContext)
                    
                    text = text.encode('utf-8')
                    html = html.encode('utf-8')
                    
                    part1 = MIMEText(text, 'plain')
                    part2 = MIMEText(html, 'html')
                    
                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    msg.attach(part1)
                    msg.attach(part2)
                    
                    reponse = mailjet.envoiMail(mail, msg)
                    return redirect('mailjet-reponse', reponse=reponse)
                else:
                    return redirect('mailjet-reponse', reponse=rep)
            else:
                # Adresse non valide
                return redirect('mailjet-reponse', reponse=0)
        else:
            return redirect('mailjet-reponse', reponse=2)
    else:
        # absence cookie
        return redirect('mailjet-reponse', reponse=4)
    
@never_cache  
def mailJetReponse(request, reponse):
    listeRep = range(0, 5)
    reponse = int(reponse)
    if reponse not in listeRep:
        raise Http404
    
    return render_to_response('lettreinformations/mailjet-reponse.html', {'reponse':reponse})

@never_cache
def mailJetGetToken(request):
    tokenCSRF = uuid.uuid1()

    reponse = HttpResponse(str(tokenCSRF), content_type="text/plain")
    reponse.set_cookie("csrftoken", tokenCSRF, 60*60*5)
    
    return reponse

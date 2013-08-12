# -*- coding: utf-8 -*-
import requests
import smtplib
import socket
from lettreinformations import settings

def addContact(mail, mailListId):
    postData = {
        'contact': mail,
        'id': mailListId,
        'force': True
    }
    
    getData = {
        'output': 'json'
    }
    
    try:
        rep = requests.post("http://api.mailjet.com/0.1/listsAddcontact", params=getData, data=postData, auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), timeout=2)
    except Timeout:
        return 2 # Erreur lors de la tentative d'ajout
    
    print rep.status_code
    
    if rep.status_code == 304:
        return 3  # Email déjà ajouté
    elif rep.status_code != 200:
        return 2 # Erreur lors de la tentative d'ajout
    else:
        repContenu = rep.json()
        if repContenu['status'] == "OK":
            return 1 # Email ajouté avec succès
        else:
            return 2 # Erreur lors de la tantative d'ajout


def isContactInList(mail, mailListId):
    getData = {
        'contact': mail,
        'output': 'json'
    }
    
    try:
        rep = requests.get("http://api.mailjet.com/0.1/contactInfos", params=getData, auth=('7462a90f3eb3bf4edc08fef33a0e6946', '24d00d8cd2d3d41dc34b8a4fc882de79'), timeout=2)
    except socket.timeout:
        return 2
    
    if rep.status_code == 204:
        return 1  # Email non enregistré
    elif rep.status_code != 200:
        return 2 # Erreur lors de la tentative d'ajout
    else:
        repContenu = rep.json()
        
        for each in repContenu['lists']:
            if each['list_id'] == mailListId and each['unsub'] == "0":
                return 3
        
        return 1
    
def envoiMail(mail, msg):
    try:
        smtpServ = smtplib.SMTP('in.mailjet.com', 587, socket.getfqdn(), 3)

        try:
            smtpServ.login(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY)
        
            try:
                
                smtpServ.sendmail('levaldyerres@levaldyerres.fr', mail, msg.as_string())
                smtpServ.quit()
                
                return 1
                
            except (smtplib.SMTPRecipientsRefused, smtplib.SMTPHeloError, smtplib.SMTPSenderRefused, smtplib.SMTPDataError):
                return 2
            
        except (smtplib.SMTPHeloError, smtplib.SMTPAuthenticationError, smtplib.SMTPException):
            return 2
            
    except (smtplib.SMTPConnectError, socket.timeout):
        return 2
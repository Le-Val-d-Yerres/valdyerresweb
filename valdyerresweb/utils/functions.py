# -*- coding: utf-8 -*-
import os, subprocess, shlex, cStringIO
import qrcode , base64, StringIO, pickle
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from PIL import Image , ImageFile
from django.utils.timezone import utc
import datetime
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import smtplib
import socket
from lettreinformations import settings as conf

ImageFile.MAXBLOCK = 2**20


def GenerationQrCode(data):
    img_io = StringIO.StringIO()
    qr = qrcode.QRCode(
                          error_correction=qrcode.constants.ERROR_CORRECT_L,
                          box_size=3,
                          border=1,
                          )
    qr.add_data(data);
    imgQr = qr.make_image()
    imgQr.save(img_io,'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue())

def serialize(item):
    itemIO = StringIO.StringIO()
    pickle.dump(item,itemIO)
    itemIO.seek(0)
    return base64.b64encode(itemIO.read())

def deserialize(base64pickleditem):
    pickleditem = base64.b64decode(base64pickleditem)
    return pickle.loads(pickleditem)


def pdftojpg(pdfFilePath, subpath = "/img/"):
    outpoutejpg = pdfFilePath.replace(".pdf",".jpg")
    head,tail = os.path.split(outpoutejpg)
    head = head+subpath
    if not os.path.exists(head):
        os.makedirs(head)
    outpoutejpg = os.path.join(head,tail)
    command_line = "pdftoppm -l 1 "+pdfFilePath
    args = shlex.split(command_line)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    mystrimage = cStringIO.StringIO(out)
    image = Image.open(mystrimage)
    image.save(outpoutejpg, "JPEG", quality=90, optimize=True, progressive=True)
    return outpoutejpg

    

# beau snippet source : http://djangosnippets.org/snippets/936/
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    print key
    if cache.has_key(key):
        cache.delete(key)
        
def resetEphemerideCache(debut):
    today = datetime.datetime.utcnow().replace(tzinfo=utc)
            
    if (debut-today).days <= 7:
        path = reverse('editorial.views.Ephemeride', kwargs={'jour':'aujourd-hui'})
        expire_page(path)
        
        path = reverse('editorial.views.Ephemeride', kwargs={'jour':'demain'})
        expire_page(path)
        
        for i in range(2, 10):
            day = datetime.datetime.today()+datetime.timedelta(days=i)
            
            slug = u""+str(day.day)+"-"+str(day.month)+"-"+str(day.year)
            
            path = reverse('editorial.views.Ephemeride', kwargs={'jour':slug})
            expire_page(path)
            
def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
def envoiMail(mail, msg):
    try:
        smtpServ = smtplib.SMTP('localhost')
        try:
            smtpServ.sendmail('levaldyerres@levaldyerres.fr', mail, msg.as_string())
            smtpServ.quit()
            
            return 1
            
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPHeloError, smtplib.SMTPSenderRefused, smtplib.SMTPDataError):
            return 2 
    except (smtplib.SMTPConnectError, socket.timeout):
        return 2

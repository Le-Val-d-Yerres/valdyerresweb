# -*- coding: utf-8 -*-
import os
import qrcode , base64, StringIO, pickle
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from PIL import Image , ImageFile

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
    outpoutepng = pdfFilePath.replace(".pdf",".png")
    head,tail = os.path.split(outpoutepng)
    head = head+subpath
    print head
    if not os.path.exists(head):
        os.makedirs(head)
    outpoutepng = os.path.join(head,tail)
    commande = "pdftoppm -png -l 1 "+pdfFilePath+" "+outpoutepng.replace(".png","")
    os.system(commande)
    tmpoutpoute = outpoutepng.replace(".png","-1.png")
    os.rename(tmpoutpoute, outpoutepng)
    image = Image.open(outpoutepng)
    outpoutejpg = outpoutepng.replace(".png",".jpg")
    image.save(outpoutejpg, "JPEG", quality=90, optimize=True, progressive=True)
    os.remove(outpoutepng)
    return outpoutejpg

    

# beau snippet source : http://djangosnippets.org/snippets/936/
def expire_page(path):
    request = HttpRequest()
    request.path = path
    key = get_cache_key(request)
    if cache.has_key(key):   
        cache.delete(key)

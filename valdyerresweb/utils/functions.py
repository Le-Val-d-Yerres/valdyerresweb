# -*- coding: utf-8 -*-

import qrcode , base64, StringIO, pickle
from django.conf import settings
import os
import ghostscript

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


def pdftojpg(pdfFilePath):
    outpoutejpg = pdfFilePath.replace(".pdf",".jpg")
    head,tail = os.path.split(outpoutejpg)
    head = head+"/img/"
    outpoutejpg = os.path.join(head,tail)
    args = ["-dSAFER",
    "-dBATCH",
    "-dNOPAUSE",
    "-sDEVICE=jpeg",
    "-r300",
    "-dJPEGQ=90",
    "-dFirstPage=1",
    "-dLastPage=1",
    "-sOutputFile="+outpoutejpg,
    pdfFilePath ]
    ghostscript.Ghostscript(*args)
    return outpoutejpg

    


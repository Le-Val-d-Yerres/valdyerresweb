# -*- coding: utf-8 -*-

import qrcode , base64, StringIO, pickle
from django.conf import settings

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


def pdftojpg(pdfFile):
    outpoutejpg = settings.MEDIA_ROOT+'uploads/magazines/'+obj.date_parution.strftime('%y%m%d-val-d-yerres-magazine.jpg')     
    fichierpdf = settings.MEDIA_ROOT+pdfFile.path
        print fichierpdf+'\r'
        print outpoutejpg+'\r'
        args = ["-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-r300",
                "-dJPEGQ=90",
                "-dFirstPage=1",
                "-dLastPage=1",
                "-sOutputFile="+outpoutejpg,
                fichierpdf ]

        ghostscript.Ghostscript(*args)
        obj.image = outpoutejpg.replace(settings.MEDIA_ROOT,"")

    


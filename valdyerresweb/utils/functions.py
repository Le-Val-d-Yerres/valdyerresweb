# -*- coding: utf-8 -*-

import qrcode , base64, StringIO, pickle

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

def serializeKwargs(kwargs):
    kwargsIO = StringIO.StringIO()
    pickle.dump(kwargs,kwargsIO)
    kwargsIO.seek(0)
    return base64.b64encode(kwargsIO.read())

def deserializeKwargs(base64pickledkwargs):
    pickledkwargs = base64.b64decode(base64pickledkwargs)
    return pickle.loads(pickledkwargs)


    


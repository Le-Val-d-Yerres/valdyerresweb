# -*- coding: utf-8 -*-
from aide.models import Aide
from django.template import Context,loader

def renderModal(aide):
    myTemplate = loader.get_template('aide/aidemodal.html')
    myContext = Context({"aide": aide})
    return myTemplate.render(myContext)
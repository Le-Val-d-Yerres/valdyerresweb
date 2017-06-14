# -*- coding: utf-8 -*-
from aide.models import Aide
from django.template import loader
from django.views.decorators.cache import cache_page


def renderModal(aide):
    myTemplate = loader.get_template('aide/aidemodal.html')
    myContext = {"aide": aide}
    return myTemplate.render(myContext)
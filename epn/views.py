from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from .models import FicheInscription
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.


def formficheinscription(request):
    params = {}
    return render_to_response('formficheinscription.html', params)

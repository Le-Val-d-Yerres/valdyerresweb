
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , redirect , get_object_or_404
from services.models import Service,PageStatiqueService,DocumentAttache




def ServiceDetail(request,service_slug):
    
    service = get_object_or_404(Service.objects.select_related(),slug = service_slug)
    pages_liees = PageStatiqueService.objects.filter(service = service.id,publie = True).select_related().order_by('index')
    
    return render_to_response('services/page-service.html', {'service' : service, 'pages_liees': pages_liees})

def PageContenu(request, service_slug ,page_slug):
    contenu = u'Home Page à faire'
    return render_to_response('editorial/home.html', {'contenu' : contenu})

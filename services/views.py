
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , redirect , get_object_or_404 , get_list_or_404
from services.models import Service,PageStatiqueService,DocumentAttache


def Services(request):
    
    services = get_list_or_404(Service)
    return render_to_response('services/services.html',{'services':services})


def ServiceDetail(request,service_slug):
    
    service = get_object_or_404(Service.objects.select_related(),slug = service_slug)
    pages_liees = PageStatiqueService.objects.filter(service = service.id,publie = True).select_related().order_by('index')
    
    return render_to_response('services/service-detail.html', {'service' : service, 'pages_liees': pages_liees})

def PageContenu(request, service_slug ,page_slug):
    
    page = get_object_or_404(PageStatiqueService.objects.select_related(), slug = page_slug, service__slug = service_slug, publie = True )
    documentattache = DocumentAttache.objects.filter(id = page.id)
    return render_to_response('services/page-service.html', {'page' : page, 'documentattache':documentattache})

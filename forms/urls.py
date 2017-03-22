from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^form-crd.html$', views.formfichestage, name="formfichestage"),
    url(r'^merci.html$', views.merci, name="merci"),
    url(r'^export-crd.csv$', views.exportcrd, name="exportcrd"),
]

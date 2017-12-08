from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^form-fiche-inscription.html$', views.formficheinscription, name="formficheinscription"),
    url(r'^inscription/(?P<uuid>[^\/]+)$', views.inscription, name='inscription'),
    url(r'^getpdf/(?P<uuid>[^\/]+)$', views.inscription, name='getpdf')

]

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^form-fiche-inscription.html$', views.formficheinscription, name="formficheinscription"),
]

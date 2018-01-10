from django.contrib import admin
from .models import FicheInscription
from django.core import urlresolvers
# Register your models here.


class FicheInscriptionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'datenaissance', 'email', 'ville', 'link_to_referent']

    def link_to_referent(self, obj):
        link = urlresolvers.reverse("admin:epn_ficheinscription_change", args=[obj.adultereferent.id])
        return u'<a href="%s">%s</a>' % (link, "telecharger pdf")
    link_to_referent.allow_tags = True

    def link_to_pdf(self, obj):
        link = urlresolvers.reverse("views:getpdf", args=[obj.uuid])
        return u'<a href="%s">%s</a>' % (link, "telecharger pdf")

    link_to_pdf.allow_tags = True


admin.site.register(FicheInscription, FicheInscriptionAdmin)
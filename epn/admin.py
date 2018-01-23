from django.contrib import admin
from .models import FicheInscription
from django.core import urlresolvers
# Register your models here.


class FicheInscriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ("adultereferent",)
    list_display = ['nom', 'prenom','numero_adherent','datenaissance', 'email', 'ville', 'link_to_pdf']
    search_fields = ['nom','numero_adherent']
    exclude = ['adultereferent']
    def link_to_referent(self, obj):
        if obj.adultereferent.id:
            link = urlresolvers.reverse("admin:epn_ficheinscription_change", args=[obj.adultereferent.id])
            nom = obj.adultereferent.nom +" "+obj.adultereferent.prenom
        else:
            link="#"
            nom = "NA"
        return u'<a href="%s">%s</a>' % (link, nom)
    link_to_referent.allow_tags = True

    def link_to_pdf(self, obj):
        link = urlresolvers.reverse("getpdf", args=[obj.uuid])
        return u'<a href="%s">%s</a>' % (link, "telecharger pdf")

    link_to_pdf.allow_tags = True


admin.site.register(FicheInscription, FicheInscriptionAdmin)
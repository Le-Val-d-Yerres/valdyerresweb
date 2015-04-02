# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from evenements.models import Evenement, DateLieuEvenement

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        evenements = Evenement.objects.all()
        for evt in evenements:
            date_lieu = DateLieuEvenement()
            date_lieu.debut = evt.debut
            date_lieu.fin = evt.fin
            date_lieu.lieu = evt.lieu
            date_lieu.evenement = evt
            date_lieu.save()


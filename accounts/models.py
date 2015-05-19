from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from services.models import Service
from evenements.models import Organisateur


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    service = models.ForeignKey(Service,null=True)
    organisateur = models.ForeignKey(Organisateur,null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from util.tools import *

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    hash = models.CharField(max_length=8, db_index=True, editable=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        hash = rand_str(size=8)
        UserProfile.objects.create(user=instance, hash=hash)

post_save.connect(create_user_profile, sender=User)


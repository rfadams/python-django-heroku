from django.db import models, utils
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from util.tools import *

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    hash = models.CharField(max_length=8, db_index=True, editable=False)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        hash = rand_str(size=8)
        try:
            UserProfile.objects.create(user=instance, hash=hash)
        except utils.DatabaseError:
            pass

post_save.connect(create_user_profile, sender=User)


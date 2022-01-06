from .models import Profile
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 

def createProfile(sender, instance, created, **kwargs):
    """
    When a user is created, profile is also created.
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            email = user.email,
            username = user.username,
            name = user.first_name
        )

def deleteUser(sender, instance, **kwargs):
    """
    When profile is deleted, user is also deleted.
    """
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)
from .models import Profile
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 

from django.conf import settings
from django.core.mail import send_mail

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

        # Send welcome email
        subject = f"Welcome {profile.name}"
        message = "Thanks for using devSearch."

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently = False
        )


def updateUser(sender, instance, created, **kwargs):
    """
    When profile is edited, user credentials are also updated.
    """
    profile = instance
    user = profile.user

    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    """
    When profile is deleted, user is also deleted.
    """
    user = instance.user
    user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
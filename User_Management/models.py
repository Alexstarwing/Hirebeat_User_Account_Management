from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='user_management_users')
    user_permissions = models.ManyToManyField(Permission, related_name='user_management_users')

    USERNAME_FIELD = 'email'

class Profile(models.Model): #model represents additional information associated with a user in Django's authentication system
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=CustomUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()
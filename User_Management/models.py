from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Permission, Group
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, is_staff=True, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return

    def get_by_natural_key(self, username):
        """
        This method is required by Django's authentication system to retrieve a user by their natural key.
        In this case, the natural key is the 'username'.
        """
        return self.get(**{self.model.USERNAME_FIELD: username})


class CustomUser(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='user_management_users')
    user_permissions = models.ManyToManyField(Permission, related_name='user_management_users')

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


# model represents additional information associated with a user in Django's authentication system
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    @receiver(post_save, sender=CustomUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

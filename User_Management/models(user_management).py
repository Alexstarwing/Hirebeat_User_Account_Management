# User_Management: Built-in Django models for authentication and session management.
# Tables for managing user data, profiles, user preferences, and settings.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission


# Description: Built-in Django User model has a custom manager that has the following helper methods (in addition to the methods provided by BaseUserManager):
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# Description: Built-in Django User model that stores the necessary information for each user, such as username, password, email, first name, last name, and date when the user joined.
class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_account_admin = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    deactivated_at = models.DateTimeField(null=True)
    is_site_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group, related_name='user_management_users')
    user_permissions = models.ManyToManyField(Permission, related_name='user_management_users')


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


# Description: Defines all the permissions available in the system, like 'can_add_job', 'can_edit_candidate', etc.
class Permission(models.Model):
    permission_name = models.CharField(max_length=255, unique=True)
    permission_type = models.CharField(max_length=255)
    permission_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'

    class Meta:
        indexes = [
            models.Index(fields=['permission_name']),
            models.Index(fields=['permission_type']),
        ]

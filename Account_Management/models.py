from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=255, unique=True, null=False)

    # define the user manager class for User
    objects = UserManager()

    # necessary to use the django authentication framework: this field is used as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

# class Profile(models.Model): #model represents additional information associated with a user in Django's authentication system
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)

#     @receiver(post_save, sender=User)
#     def update_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#             instance.profile.save()
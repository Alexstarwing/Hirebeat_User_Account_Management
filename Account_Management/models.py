from django.db import models
from User_Management.models import Profile

# Create your models here.


class Account(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    office = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    profile_logo = models.ImageField(null=True, blank=True)
    # def __str__(self):
    #     users = self.users.all()
    #     first_user = users[0].name if users else 'No users'
    #     return f'{first_user}, Organization: {self.organization}, Office: {self.office}, Department: {self.department}'
    
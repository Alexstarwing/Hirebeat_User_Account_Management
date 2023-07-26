from django.db import models
from User_Management.models import Profile

# Create your models here.


class Account(models.Model):
    users = models.ManyToManyField(Profile)
    office = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        users = self.users.all()
        first_user = users[0].name if users else 'No users'
        return f'{first_user}, Office: {self.office}, Department: {self.department}'




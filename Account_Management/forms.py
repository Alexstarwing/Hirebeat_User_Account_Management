from django import forms
from django.forms import ModelForm
from .models import *


class InviteForm(forms.Form):
    # name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True, label='Email')
    role_name = forms.CharField(max_length=255)
    role_type = forms.ChoiceField(choices=Role.ROLE_TYPE_CHOICES)


class OrganizationForm(forms.Form): 
    organization = forms.CharField(max_length=200, label='Organization Name')


class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=200, label='First name')
    last_name = forms.CharField(max_length=200, label='Last name')


class RegisterWithInvitationForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True, label='Email')
    role_type = forms.ChoiceField(choices=Role.ROLE_TYPE_CHOICES)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label='Confirm Password')

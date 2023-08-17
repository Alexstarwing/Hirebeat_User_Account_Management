from django import forms
from .models import Profile, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# from django.contrib.auth.models import User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}),
                             label='Email'
                             )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}),
        label='Username'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}),
        label='Password1'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}),
        label='Password2'
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# class ResendActivationEmailForm(forms.Form):
#     email = forms.EmailField(required=True)

class CustonmerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-prepended'}),
        label='Username'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-prepended'}),
        label='Password'
    )


class UpdateEmailForm(forms.Form):
    new_email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'shadow-border'}), label='new email')


class VerificationForm(forms.Form):
    verification_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'shadow-border'}),
                                        max_length=20, label='Verification Code')


class UserInfoForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'shadow-border'}),
                                 max_length=200, label='First name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'shadow-border'}),
                                max_length=200, label='Last name')

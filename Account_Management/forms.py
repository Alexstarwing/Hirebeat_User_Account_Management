from django import forms


class InviteForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True, label='Email')

class OrganizationForm(forms.Form): 
    organization = forms.CharField(max_length=200, label='Organization Name')
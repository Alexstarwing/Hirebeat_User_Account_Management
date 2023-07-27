from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from Account_Management.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views import View
from .forms import InviteForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator


class AccountList(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'Accounts'


class EditAccountView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'edit_account'
    template_name = 'Account_Management/edit_account.html'


class SettingView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'settings'
    template_name = 'Account_Management/settings.html'


class AddUserView(LoginRequiredMixin, View):
    model = Account
    context_object_name = 'add_user'
    template_name = 'Account_Management/add_user.html'

    def get(self, request):
        form = InviteForm()  # Create an instance of the InviteForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InviteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # Generate the registration link
            current_site = get_current_site(self.request)
            uid = urlsafe_base64_encode(force_bytes(email))
            register_link = f"https://{current_site.domain}/register"

            # Send invitation email with registration link
            subject = 'Invitation to Register'
            message = f'Hi {name}, you have been invited to register on our website. Please use the following link to ' \
                      f'register: {register_link}'
            from_email = 'yifandsb666@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('account_management:invitation')
        else:
            return render(request, self.template_name, {'form': form})


class InvitationView(LoginRequiredMixin, View):
    template_name = 'Account_Management/invitation.html'

    def get(self, request):
        return render(request, self.template_name)


class OrganizationView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'organization'
    template_name = 'Account_Management/organization.html'

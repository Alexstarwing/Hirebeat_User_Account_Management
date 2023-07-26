import pdb
from django.http import HttpResponse
from typing import Any, Dict
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserCreationForm#, ResendActivationEmailForm
from .models import Profile
from .tokens import account_activation_token


class CustomLoginView(LoginView):
    template_name = 'User_Management/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profiles')


class RegisterPage(FormView):
    template_name = 'User_Management/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profiles')  # where user will be redirect after success registration

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('User_Management/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        send_mail(mail_subject, message, 'yifandsb666@gmail.com', [user.email])
        email_sent_message = "Activation email has been sent to your email address."  # flash message
        messages.success(self.request, email_sent_message)
        #return redirect('resend_activation_email') #Notify about the sent in another page
        return super().form_valid(form)  # Redirect to success_url

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profiles')  # Redirect to the home page
        return super().get(*args, **kwargs)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # pdb.set_trace()  # 断点
        if user is not None and default_token_generator.check_token(user, token):  
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            # login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')


class ProfileList(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'profiles'
    
class EditAccountView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'edit-account'
    template_name = 'User_Management/edit-account.html'
    
class SettingView(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'author-settings'
    template_name = 'User_Management/author-settings.html'

# def resend_activation_email(request): 
#     if request.user.is_authenticated:
#         return redirect('profiles')
    
#     form = ResendActivationEmailForm(request.POST)
#     if form.is_valid():
#         email = form.cleaned_data["email"]
#         user = User.objects.filter(email=email, is_active=0)

#         if not user.count():
#             form._errors["email"] = ["Account for email address is not registered or already activated."]

#         token = default_token_generator.make_token(user)
#         current_site = get_current_site(request)
#         mail_subject = 'Activate your account'
#         message = render_to_string('User_Management/account_activation_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': token,
#         })
#         send_mail(mail_subject, message, 'yifandsb666@gmail.com', [user.email])
#         return redirect('resend_activation_email') 
    
#     return HttpResponse("An error occurred or the form is not valid.")

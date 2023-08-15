import pdb
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string

from .decorators import admin_required
from django.http import HttpResponse
from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserCreationForm, CustomLoginForm  # , ResendActivationEmailForm
from .models import Profile, CustomUser
from Account_Management.models import Account, AccountUserRelation
from django.contrib.auth.models import Group
from .tokens import account_activation_token


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'User_Management/login_1.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('profiles')


class RegisterPage(FormView):
    template_name = 'User_Management/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profiles')  # where user will be redirect after success registration

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_staff = True
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
        # pdb.set_trace()
        email_sent_message = "Activation email has been sent to your email address."  # flash message
        messages.success(self.request, email_sent_message)
        admin_group = Group.objects.get(name='Admin Group')  # Replace 'admin' with your actual group name
        user.groups.add(admin_group)
        # return redirect('resend_activation_email') #Notify about the sent in another page
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('profiles')  # Redirect to the home page
        return super().get(*args, **kwargs)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        # pdb.set_trace()  # 断点
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()

            desired_domin = 'http://www.domin/' + get_random_string(32)
            account = Account.objects.create(company_domain=desired_domin)
            AccountUserRelation.objects.create(account=account, user=user)

            # login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('login')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('register')


class ProfileList(LoginRequiredMixin, ListView):
    model = Profile
    context_object_name = 'profiles'

    def get_user_roles(self):
        user = self.request.user
        user_groups = user.groups.all()
        user_roles = [group.name for group in user_groups]
        # pdb.set_trace()  # 断点
        return force_text(user_roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_roles = self.get_user_roles()
        context['user_roles'] = user_roles

        # get user's firstname and lastname
        current_user = self.request.user
        first_name = current_user.first_name
        last_name = current_user.last_name

        # put firstname and lastname in context
        context['first_name'] = first_name
        context['last_name'] = last_name

        account_relation = AccountUserRelation.objects.filter(user=self.request.user).first()
        if account_relation:
            context['account'] = account_relation.account
        return context

    # return (reverse('account_management:account'))


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


def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    # Retrieve all related users
    account_user_relations = AccountUserRelation.objects.filter(account=account)
    users_to_delete = [relation.user for relation in account_user_relations]

    if request.method == 'POST':
        # Delete all related AccountUserRelation entries
        account_user_relations.delete()

        # Delete all related users
        for user in users_to_delete:
            user.delete()

        # Delete the account itself
        account.delete()

        email_sent_message = "Your Account Has Been Deleted!"
        messages.success(request, email_sent_message)

        return redirect('login')

from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from Account_Management.models import Account, TeamInvitation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views import View
from .forms import InviteForm, OrganizationForm
from Account_Management.models import Profile, Account, AccountUserRelation
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from .models import Role


class AccountList(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'Accounts'


class EditAccountView(LoginRequiredMixin, View):
    model = Account
    context_object_name = 'edit_account'
    template_name = 'Account_Management/edit_account.html'

    def get_account_for_user(self, user):
        try:
            account_user_relation = AccountUserRelation.objects.get(user=user)
            return account_user_relation.account
        except AccountUserRelation.DoesNotExist:
            return None

    def get(self, request):
        current_user = request.user
        account = self.get_account_for_user(current_user)

        if not account:
            raise Http404("No account linked with the current user.")
        
        form = OrganizationForm(initial={'organization': account.organization})
        return render(request, self.template_name, {'form': form})
    
        # try:
        #     profile = Profile.objects.get(user=request.user)
        #     account = Account.objects.filter(profile=profile).first()
        #     form = OrganizationForm(initial={'organization': account.organization}) if account else OrganizationForm()
        # except Profile.DoesNotExist:
        #     form = OrganizationForm()
        
        # return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = OrganizationForm(request.POST)
        if form.is_valid():
            current_user = request.user
            account = self.get_account_for_user(current_user)

            if not account:
                raise Http404("No account linked with the current user.")
            # profile = Profile.objects.get(user=request.user)
            # account, created = Account.objects.get_or_create(profile=profile)
            account.organization = form.cleaned_data['organization']
            account.save()
            return redirect('account_management:edit_account') 
        return render(request, self.template_name, {'form': form})

class SettingView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'settings'
    template_name = 'Account_Management/settings.html'


class AddUserView(LoginRequiredMixin, View):
    model = TeamInvitation
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
            register_link = f"http://{current_site.domain}/register"

            # Send invitation email with registration link
            subject = 'Invitation to Register'
            message = render_to_string('Account_Management/account_activation_email.html', {
                'user': name,
                'register_link': register_link,
            })
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
    
    def get_account_for_user(self, user):
        try:
            account_user_relation = AccountUserRelation.objects.get(user=user)
            return account_user_relation.account
        except AccountUserRelation.DoesNotExist:
            return None
        
    def account_detail(self, request):
        current_user = request.user
        account = self.get_account_for_user(current_user)

        if not account:
            raise Http404("No account linked with the current user.")
        # try:
        #     account = Account.objects.get(profile__user=request.user)
        # except Account.DoesNotExist:
        #     account = None

        return render(request, 'organization.html', {'account': account})

class ManageUserView(View):
    model = Account
    template_name = 'Account_Management/manage_user.html'
    assign_org_url = reverse_lazy('account_management:edit_account')

    def get_account_for_user(self, user):
        try:
            account_user_relation = AccountUserRelation.objects.get(user=user)
            return account_user_relation.account
        except AccountUserRelation.DoesNotExist:
            return None
        
    def dispatch(self, request, *args, **kwargs):
        try:
            current_account = self.get_account_for_user(request.user)
            # current_account = Account.objects.get(profile__user=request.user)
        
            # Check if organization name is assigned, if not, redirect with a message
            if not current_account:#.organization:
                messages.warning(request, "Please assign an organization first.")
                return redirect(self.assign_org_url)
        except AccountUserRelation.DoesNotExist: #except Account.DoesNotExist: 
                messages.warning(request, "Please assign an organization first.")
                return redirect(self.assign_org_url)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request): 
        current_account = self.get_account_for_user(request.user)
        accounts = AccountUserRelation.objects.filter(account=current_account)
        return render(request, self.template_name, {'accounts': accounts})

    # def get(self, request):
    #     current_account = self.get_account_for_user(request.user)
    #     # current_account = Account.objects.get(profile__user=request.user)
    #     accounts = Account.objects.filter(organization=current_account.organization)
    #     return render(request, self.template_name, {'accounts': accounts})
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     current_account = self.get_account_for_user(self.request.user)
    #     if current_account:
    #         usernames = list(AccountUserRelation.objects.filter(account=current_account).values_list('user__username', flat=True))
    #         context['usernames'] = usernames
    #     return context
    
def acccountSettings(request):
    context = {}
    return render(request, 'accounts/origanization.html', context)




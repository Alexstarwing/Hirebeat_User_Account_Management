import pdb

from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
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
from django.utils.crypto import get_random_string
from User_Management.models import CustomUser
from .forms import InviteForm, OrganizationForm, RegisterWithInvitationForm
from User_Management.forms import UserCreationForm
from Account_Management.models import Profile, Account, AccountUserRelation
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from .models import Role
from django.contrib.auth.models import Group


class AccountList(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'Accounts'


class AccountSettingView(LoginRequiredMixin, View):
    model = Account
    context_object_name = 'edit_account'
    template_name = 'Account_Management/edit_account.html'

    def get_account_for_user(self, user):
        try:
            account_user_relation = AccountUserRelation.objects.get(user=user)
            # pdb.set_trace()
            return account_user_relation.account
        except AccountUserRelation.DoesNotExist:
            return None

    def get(self, request):
        current_user = request.user
        account = self.get_account_for_user(current_user)

        if not account:
            raise Http404("No account linked with the current user.")

        form = OrganizationForm(initial={'organization': account.organization})
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]

        return render(request, self.template_name, {'form': form, 'user_roles': user_roles[0]})

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


class ConfigureView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'settings'

    def get_user_role(self, request, *args, **kwargs):
        # pdb.set_trace()
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        return force_str(user_roles)

    def get_context_data(self, **kwargs):
        context = super(ConfigureView, self).get_context_data()
        user_roles = self.get_user_role(self.request)
        context['user_roles'] = user_roles
        return context


class AddUserView(LoginRequiredMixin, View):
    model = TeamInvitation
    context_object_name = 'add_user'
    template_name = 'Account_Management/add_user.html'
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
            if not current_account.organization:
                messages.warning(request, "Please assign an organization first.")
                return redirect(self.assign_org_url)
        except AccountUserRelation.DoesNotExist:
            messages.warning(request, "Please assign an organization first.")
            return redirect(self.assign_org_url)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = InviteForm()  # Create an instance of the InviteForm
        # get role
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        # pdb.set_trace()  # 断点
        return render(request, self.template_name, {'form': form, 'user_roles': user_roles[0]})

    def post(self, request):
        form = InviteForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            role_name = form.cleaned_data['role_name']
            role_type = form.cleaned_data['role_type']

            role = Role.objects.create(role_name=role_name, role_type=role_type)

            account_user_relation = AccountUserRelation.objects.get(user=request.user)
            account = account_user_relation.account

            # Generate the invitation token
            invitation_token = get_random_string(32)
            # invitation_token = default_token_generator.make_token(request.user)
            # print(invitation_token)

            # Save the invitation with the token and other data
            invitation = TeamInvitation(
                account=account,
                invited_email=email,
                invited_by_user=request.user,
                role=role,
                invitation_token=invitation_token,
            )
            invitation.save()

            # Generate the registration link
            current_site = get_current_site(self.request)
            # uid = urlsafe_base64_encode(force_bytes(email))
            # register_link = f"http://{current_site.domain}/register"
            # register_link = reverse('account_management:register_with_invitation', args=[invitation_token])

            # Send invitation email with registration link
            subject = 'Invitation to Register'
            message = render_to_string('Account_Management/account_activation_email.html', {
                # 'user': name,
                'domain': current_site.domain,
                'invitation_token': invitation_token,
                # 'register_link': register_link,
            })
            from_email = 'yifandsb666@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('account_management:invitation')
        else:
            return render(request, self.template_name, {'form': form})


class RegisterWithInvitationView(View):
    template_name = 'Account_Management/register_with_invitation.html'

    def get(self, request, invitation_token):
        # Decode the uidb64 and check if the invitation is valid
        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            self.team_invitation = TeamInvitation.objects.get(
                invitation_token=invitation_token)
            # (id=uid, invitation_token=invitation_token) but no id field inside TeamInvitation model
        except TeamInvitation.DoesNotExist:  # (TypeError, ValueError, OverflowError, TeamInvitation.DoesNotExist):
            messages.error(request, "Invalid invitation link.")
            # return redirect('account_management:invalid_invitation')

        # return redirect('user_management:register')
        # form = RegisterWithInvitationForm()
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, invitation_token):
        try:
            team_invitation = TeamInvitation.objects.get(invitation_token=invitation_token)
        except (TypeError, ValueError, OverflowError, TeamInvitation.DoesNotExist):
            messages.error(request, "Invalid invitation link.")
            return redirect('account_management:invalid_invitation')

        def clean(self):
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                raise form.ValidationError("Passwords do not match. Please enter the same password in both fields.")

            return cleaned_data

        # form = RegisterWithInvitationForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            new_user = CustomUser.objects.create_user(username=username, email=email, password=password)
            new_user.is_active = True
            new_user.save()
            # team_invitation.user = new_user

            role = team_invitation.role
            group_name = f"{role.role_type.capitalize()} Group"
            associated_group = Group.objects.get(name=group_name)
            new_user.groups.add(associated_group)

            AccountUserRelation.objects.create(account=team_invitation.account, user=new_user)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('/login/')
        else:
            return render(request, self.template_name, {'form': form})


class InvitationView(LoginRequiredMixin, View):
    template_name = 'Account_Management/invitation.html'

    def get(self, request):
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        # pdb.set_trace()  # 断点
        return render(request, self.template_name, {'user_roles': user_roles[0]})


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

        return render(request, self.template_name, {'account': account})

    def get(self, request):
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        return render(request, self.template_name, {'user_roles': user_roles[0]})


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
            if not current_account.organization:
                messages.warning(request, "Please assign an organization first.")
                return redirect(self.assign_org_url)
        except AccountUserRelation.DoesNotExist:  # except Account.DoesNotExist:
            messages.warning(request, "Please assign an organization first.")
            return redirect(self.assign_org_url)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        current_account = self.get_account_for_user(request.user)
        accounts = AccountUserRelation.objects.filter(account=current_account)
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        # user_role_data = []  # To store user and corresponding role data

        # for account in accounts:
        #     user = account.user  # Get the user associated with the AccountUserRelation
        #     team_invitation = TeamInvitation.objects.get(user=user)  # Use .filter() to avoid DoesNotExist

        #     if team_invitation:
        #         user_role_data.append({'user': user, 'role': team_invitation.role})

        # context = {
        #     'user_role_data': user_role_data,
        # }

        # return render(request, self.template_name, context)
        return render(request, self.template_name, {'accounts': accounts, 'user_roles': user_roles[0]})

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

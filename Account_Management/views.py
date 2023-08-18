import pdb
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from Account_Management.models import Account, TeamInvitation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.utils.crypto import get_random_string
from User_Management.models import CustomUser
from .forms import InviteForm, OrganizationForm, UserInfoForm
from User_Management.forms import UserCreationForm
from Account_Management.models import Profile, Account, AccountUserRelation
from django.template.loader import render_to_string
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
            return account_user_relation.account
        except AccountUserRelation.DoesNotExist:
            return None

    def get(self, request):
        current_user = request.user
        account = self.get_account_for_user(current_user)

        if not account:
            raise Http404("No account linked with the current user.")

        org_form = OrganizationForm(initial={'organization': account.organization})
        user_info_form = UserInfoForm(
            initial={'first_name': current_user.first_name, 'last_name': current_user.last_name})
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        # account_user_relation = AccountUserRelation.objects.filter(user=current_user).first()
        # company_name = account_user_relation.account.company_name
        company_name = get_company_name(current_user)

        return render(request, self.template_name, {
            'account': account,
            'org_form': org_form,
            'user_info_form': user_info_form,
            'user_roles': user_roles[0],
            'company_name': company_name,
        })

    def post(self, request):
        org_form = OrganizationForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if user_info_form.is_valid():
            current_user = request.user

            current_user.first_name = user_info_form.cleaned_data['first_name']
            current_user.last_name = user_info_form.cleaned_data['last_name']
            current_user.save()
            return redirect('account_management:edit_account')
        if org_form.is_valid():
            current_user = request.user
            account = self.get_account_for_user(current_user)

            if not account:
                raise Http404("No account linked with the current user.")
            # profile = Profile.objects.get(user=request.user)
            # account, created = Account.objects.get_or_create(profile=profile)
            account.organization = org_form.cleaned_data['organization']
            account.save()
            return redirect('account_management:edit_account')
        else:
            self.create_or_update_employer_basic_info(request)
            self.create_or_update_employer_info(request)
            self.create_or_update_employer_summary(request)

        #return render(request, self.template_name, {'org_form': org_form})
        # Thinking of rediect user to organiztion, which view the changes.
        # return render(request, 'Account_Management/organization.html', {'org_form': org_form})
        return redirect('account_management:edit_account')

    def create_or_update_employer_basic_info(self, request):
        if request.method == 'POST':
            company_domain = request.POST.get("user_id")
            company_industry = request.POST.get("company_type")
            company_email = request.POST.get("contactEmail")
            company_location = request.POST.get("location")
            company_size_range = request.POST.get("company_size")

            account, created = Account.objects.get_or_create(
                company_domain=company_domain,
                defaults={
                    'company_industry': company_industry,
                    'company_email': company_email,
                    'company_location': company_location,
                    'company_size_range': company_size_range
                }
            )

            if not created:
                account.company_industry = company_industry
                account.company_email = company_email
                account.company_location = company_location
                account.company_size_range = company_size_range
                account.save()
                messages.success(request, 'Your basic information has been successfully updated. ',
                                 extra_tags='basic_info')
            else:
                pass
                
        return redirect('account_management:organization')

    def create_or_update_employer_info(self, request):
        if request.method == 'POST':
            company_domain = request.POST.get("user_id")
            company_name = request.POST.get("name")
            company_website = request.POST.get("website")

            account, created = Account.objects.get_or_create(
                company_domain=company_domain,
                defaults={
                    'company_name': company_name,
                    'company_website': company_website,
                }
            )

            if not created:
                account.company_name = company_name
                account.company_website = company_website
                account.save()
                messages.success(request, 'Your information has been successfully updated. ',
                                 extra_tags='info')
            else:
                pass
                
            #return render(request, 'Account_Management/edit_account.html', {'extra_tags': 'info'})
        return redirect('account_management:organization')
        
        # create_or_update_employer_summary: Creates or updates an employer's summary or description
    def create_or_update_employer_summary(self, request):
        company_domain = request.POST.get("user_id")
        company_summary = request.POST.get("summary")

        account, created = Account.objects.get_or_create(
            company_domain=company_domain,
            defaults={
            'company_summary': company_summary,
            }
        )

        if not created:
            account.company_summary = company_summary
            account.save()
            messages.success(request, 'Your summary has been successfully updated. ',
                                 extra_tags='summary')
            
        return redirect('account_management:organization')




class ConfigureView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'settings'

    def get_user_role(self, request, *args, **kwargs):
        current_user = request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        return force_str(user_roles)

    def get_context_data(self, **kwargs):
        context = super(ConfigureView, self).get_context_data()
        user_roles = self.get_user_role(self.request)
        current_user = self.request.user
        account = getAccount(current_user)
        context['user_roles'] = user_roles
        context['account'] = account
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
        form = InviteForm()
        # get role
        current_user = request.user
        account = getAccount(current_user)
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]
        return render(request, self.template_name, {'form': form, 'user_roles': user_roles[0], 'account': account})

    def post(self, request):
        form = InviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            role_name = form.cleaned_data['role_name']
            role_type = form.cleaned_data['role_type']

            role = Role.objects.create(role_name=role_name, role_type=role_type)

            account_user_relation = AccountUserRelation.objects.get(user=request.user)
            account = account_user_relation.account

            # Generate the invitation token
            invitation_token = get_random_string(32)

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

            # Send invitation email with registration link
            subject = 'Invitation to Register'
            message = render_to_string('Account_Management/account_activation_email.html', {
                'domain': current_site.domain,
                'invitation_token': invitation_token,
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
            self.team_invitation = TeamInvitation.objects.get(
                invitation_token=invitation_token)
        except TeamInvitation.DoesNotExist:  # (TypeError, ValueError, OverflowError, TeamInvitation.DoesNotExist):
            messages.error(request, "Invalid invitation link.")

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
        account = self.get_account_for_user(current_user)
        company_name = get_company_name(current_user)
        company_name_exists = check_company_name_existence(company_name)
        return render(request, self.template_name, {'user_roles': user_roles[0], 'company_name': company_name,
                                                    'company_name_exists': company_name_exists, 'account': account})


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
        return render(request, self.template_name, {'accounts': accounts, 'user_roles': user_roles[0],
                                                    'account': current_account})


def acccountSettings(request):
    context = {}
    return render(request, 'accounts/origanization.html', context)


# create_or_update_employer_social_media: Creates or updates an employer's social media profiles
@api_view(['POST'])
def create_or_update_employer_social_media(request):
    company_domain = request.data["user_id"]
    company_linkedin = request.data["linkedin"]
    company_facebook = request.data["facebook"]
    company_twitter = request.data["twitter"]

    account, created = Account.objects.get_or_create(
        company_domain=company_domain,
        defaults={
            'company_linkedin': company_linkedin,
            'company_facebook': company_facebook,
            'company_twitter': company_twitter
        }
    )

    if not created:
        account.company_linkedin = company_linkedin
        account.company_facebook = company_facebook
        account.company_twitter = company_twitter
        account.save()

    return Response("Create or Update employer social media successfully", status=status.HTTP_201_CREATED)


def delete_account(request, account):
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


def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('login'))


def getAccount(user):
    account_user_relation = AccountUserRelation.objects.filter(user=user).first()
    return account_user_relation.account


def get_company_name(user):
    account = getAccount(user)
    company_name = account.organization
    # company_name = account.company_name
    return company_name


def check_company_name_existence(target_name):
    if Account.objects.filter(organization=target_name).exists():
    # if Account.objects.filter(company_name=target_name).exists():
        return "Company name is existed"
    else:
        return "Company name is brand new!"

# create_or_update_employer_basic_info: Creates or updates basic information for an employer's profile
# def create_or_update_employer_basic_info(request):
#     if request.method == 'POST':
#         company_domain = request.POST.get("user_id")
#         company_industry = request.POST.get("company_type")
#         company_email = request.POST.get("contactEmail")
#         company_location = request.POST.get("location")
#         company_size_range = request.POST.get("company_size")

#         account, created = Account.objects.get_or_create(
#             company_domain=company_domain,
#             defaults={
#             'company_industry': company_industry,
#             'company_email': company_email,
#             'company_location': company_location,
#             'company_size_range': company_size_range
#             }
#         )

#         if not created:
#             account.company_industry = company_industry
#             account.company_email = company_email
#             account.company_location = company_location
#             account.company_size_range = company_size_range
#             account.save()
#         return redirect('account_management:organization')
#     else:
#         # Return a form for GET requests
#         return render(request, 'Account_Management/basic_info.html')

# def create_or_update_employer_info(request):
#         if request.method == 'POST':
#             company_domain = request.POST.get("user_id")
#             company_name = request.POST.get["name"]
#             company_website = request.POST.get["website"]

#             account, created = Account.objects.get_or_create(
#                 company_domain=company_domain,
#                 defaults={
#                 'company_name': company_name,
#                 'company_website': company_website,
#                 }
#             )

#             if not created:
#                 account.company_name = company_name
#                 account.company_website = company_website
#                 account.save()

#             return redirect('account_management:organization')
#         else:
#             # Return a form for GET requests
#             return render(request, 'Account_Management/edit_account.html')

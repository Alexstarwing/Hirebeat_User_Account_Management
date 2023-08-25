import pdb
import random
import re
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserCreationForm, CustomLoginForm, UpdateEmailForm, UserInfoForm, UpdatePasswordForm, \
    VerificationForm, ResendActivationEmailForm
from .models import Profile, CustomUser
from Account_Management.models import Account, AccountUserRelation, TeamInvitation
from django.contrib.auth.models import Group


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'User_Management/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.get_user()

        if user.is_authenticated:
            user_email = user.email
            invitation_exists = TeamInvitation.objects.filter(invited_email=user_email).exists()

            if invitation_exists:
                invitation_account = TeamInvitation.objects.filter(invited_email=user_email).first()
                account_user_relation = AccountUserRelation.objects.filter(user=user).first()

                if account_user_relation:
                    account = account_user_relation.account
                    other_users_count = AccountUserRelation.objects.filter(account=account).exclude(user=user).count()
                    
                    if other_users_count == 0:
                        role_type = invitation_account.role.role_type.capitalize()
                        role_type += " Group"
                        group_instance = Group.objects.get(name=role_type)
                        user.groups.set([group_instance])
                        # Delete the old account (if desired)
                        if account_user_relation.account:
                            account_user_relation.account.delete()

                        # Assign the new account from the invitation
                        account_user_relation.account = invitation_account.account
                        account_user_relation.save()
                        
                        

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profiles')


class RegisterPage(FormView):
    template_name = 'User_Management/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profiles')  # where user will be redirect after success registration

    # email_sent = False

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
        self.request.session['email_sent'] = True
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
        if 'email_sent' in self.request.session:
            del self.request.session['email_sent']
        # resend_verification = self.request.GET.get('resend_verification')
        # if resend_verification == 'true':
        #     return self.resend_activation_email()
        return super().get(*args, **kwargs)

    # def post(self, *args, **kwargs):
    #     if "create_account" in self.request.POST:
    #         return self.form_valid(self.get_form())  # Manually call form_valid for account creation
    #     elif "resend_verification" in self.request.POST:
    #         return self.resend_activation_email()
    #     else:
    #         return super().post(*args, **kwargs)

    # def resend_activation_email(self):
    #     if self.email_sent:
    #         user = self.request.user 
    #         if not user.is_active:
    #             token = default_token_generator.make_token(user)
    #             current_site = get_current_site(self.request)
    #             mail_subject = 'Resend Activation Email'
    #             message = render_to_string('User_Management/account_activation_email.html', {
    #                 'user': user,
    #                 'domain': current_site.domain,
    #                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #                 'token': token,
    #             })
    #             send_mail(mail_subject, message, 'yifandsb666@gmail.com', [user.email])
    #             email_sent_message = "Activation email has been resent to your email address."
    #             messages.success(self.request, email_sent_message)
    #         else:
    #             messages.warning(self.request, "Account is already active or user is not authenticated.")
    #     else:
    #         messages.warning(self.request, "Please submit the form first to initiate the verification email.")

    #     return self.render_to_response(self.get_context_data(form=self.form))


class ResendActivationView(FormView):
    template_name = 'User_Management/resend_activation.html'
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = self.request.user
        try:
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
        except CustomUser.DoesNotExist:
            messages.error(self.request, "No account with this email exists.")
            return super().form_valid(form)

        if not user.is_active:
            token = default_token_generator.make_token(user)
            current_site = get_current_site(self.request)
            mail_subject = 'Resend Activation Email'
            message = render_to_string('User_Management/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            send_mail(mail_subject, message, 'yifandsb666@gmail.com', [user.email])
            email_sent_message = "Activation email has been resent to your email address."
            messages.success(self.request, email_sent_message)
        else:
            messages.warning(self.request, "Account is already active.")

        return super().form_valid(form)


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        # pdb.set_trace()  # 断点
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_staff = False
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
        return force_str(user_roles)

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


def check_password_strength(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long. Please try again."

    if not re.search(r'\d', password):
        return "Password must contain at least one digit. Please try again."

    if not re.search(r'[a-zA-Z]', password):
        return "Password must contain at least one letter. Please try again."

    return "Password meets the complexity requirements."


class UserSettingView(LoginRequiredMixin, View):
    model = Profile
    context_object_name = 'user_settings'
    template_name = 'User_Management/user_setting.html'

    def get(self, request):
        current_user = request.user

        # forms render
        user_info_form = UserInfoForm(
            initial={'first_name': current_user.first_name, 'last_name': current_user.last_name})
        update_email_form = UpdateEmailForm(initial={'new_email': current_user.email})
        update_password_form = UpdatePasswordForm(initial={'old_password': current_user.password})

        # get user's role
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]

        # delete account function
        account_user_relation = AccountUserRelation.objects.filter(user=current_user).first()
        account = account_user_relation.account

        return render(request, self.template_name, {
            'user_info_form': user_info_form,
            'update_email_form': update_email_form,
            'update_password_form': update_password_form,
            'account': account,
            'user_roles': user_roles[0]})

    def post(self, request):
        current_user = request.user
        user_info_form = UserInfoForm(request.POST)
        update_email_form = UpdateEmailForm(request.POST)
        update_password_form = UpdatePasswordForm(request.POST)

        if user_info_form.is_valid():
            current_user.first_name = user_info_form.cleaned_data['first_name']
            current_user.last_name = user_info_form.cleaned_data['last_name']
            current_user.save()
            return redirect('user_setting')

        if update_email_form.is_valid():
            new_email = update_email_form.cleaned_data['new_email']

            # generate a 6-digit verification code
            verification_code = "".join(random.choices('0123456789', k=6))

            # send the verification email
            send_mail(
                'Email Verification Code | HireBeat',
                f'Your Verification Code is: {verification_code}',
                'yifandsb666@gmail.com',
                [new_email],
                fail_silently=False,
            )

            # save the verification_code and the new email address in session
            self.request.session['verification_code'] = verification_code
            self.request.session['new_email'] = new_email
            return redirect('verify_code')

        if update_password_form.is_valid():
            old_password = update_password_form.cleaned_data['old_password']
            if not current_user.check_password(old_password):
                messages.error(request, "Old message type in incorrect. Please try again", extra_tags='password')
            else:
                new_password1 = update_password_form.cleaned_data['new_password1']
                new_password2 = update_password_form.cleaned_data['new_password2']
                password_check_result = check_password_strength(new_password1)
                if password_check_result != "Password meets the complexity requirements.":
                    messages.error(self.request, password_check_result, extra_tags='password')
                elif new_password1 != new_password2:
                    messages.error(request, "Two passwords don't match. Please try again.", extra_tags='password')
                else:
                    current_user.set_password(new_password1)
                    current_user.save()

                    # Update session auth hash to keep the user logged in
                    update_session_auth_hash(request, current_user)

                    send_mail(
                        'Your password has been changed',
                        'We noticed the password for your Greenhouse account was recently changed. '
                        'If this was you, you can ignore this email – we’re just checking in.'
                        'If it wasn’t you, please reset your password to keep your account secure.',
                        'yifandsb666@gmail.com',
                        [current_user.email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Your password has been successfully updated. '
                                              'Remember to keep your password secure and avoid sharing it with anyone.',
                                     extra_tags='password')

        return redirect('user_setting')


class VerifyCodeView(FormView):
    template_name = 'User_Management/verify_code.html'
    context_object_name = 'verify_code'

    def get(self, request, *args, **kwargs):
        # get user's role
        current_user = self.request.user
        user_groups = current_user.groups.all()
        user_roles = [group.name for group in user_groups]

        # delete account function
        account_user_relation = AccountUserRelation.objects.filter(user=current_user).first()
        account = account_user_relation.account
        verify_form = VerificationForm()
        return render(request, self.template_name, {'verify_form': verify_form,
                                                    'account': account,
                                                    'user_roles': user_roles[0]})

    def post(self, request, *args, **kwargs):
        verify_form = VerificationForm(request.POST)
        if verify_form.is_valid():
            # pdb.set_trace()
            current_user = self.request.user
            user_entered_code = verify_form.cleaned_data['verification_code']
            stored_code = self.request.session.get('verification_code')
            new_email = self.request.session.get('new_email')

            # verify whether is code is correct
            if stored_code == user_entered_code:
                # update email in TeamInvitation
                current_user = self.request.user
                user_groups = current_user.groups.all()
                user_roles = [group.name for group in user_groups]
                if force_str(user_roles) != "['Admin Group']":
                    TeamInvitation.objects.filter(invited_email=current_user.email).update(invited_email=new_email)

                current_user.email = new_email
                current_user.save()

                TeamInvitation.objects.filter(user=current_user).update(invited_email=new_email)
                teamInvitation = TeamInvitation.objects.filter(user=current_user)
                for element in teamInvitation:
                    if element == 'invited_email':
                        print('have invited email')
                    else:
                        print(element)
                # pdb.set_trace()
                messages.success(self.request, 'Congratulations! Your email address has been successfully updated.',
                                 extra_tags='email')
                return redirect('user_setting')
            else:
                messages.error(self.request, 'Invalid verification code. Please try again.')
                return redirect('verify_code')

        return self.form_invalid(verify_form)


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


def update_company_name(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        account.company_name = company_name
        account.save()
    return redirect('login')  # Redirect to the desired page after submission


class UpdateEmployerLogoView(LoginRequiredMixin, View):
    template_name = 'User_Management/upload_employer_logo.html'

    def get(self, request):
        current_user = self.request.user
        account_user_relation = AccountUserRelation.objects.filter(user=current_user).first()
        account = account_user_relation.account
        return render(request, 'User_Management/upload_employer_logo.html', {'user': current_user, 'account': account})







# def update_company_name(request, user):
#     relation = AccountUserRelation.objects.filter(user=user).first()
#     if relation:
#         if request.method == 'POST':
#             account = relation.account
#             company_name = request.POST.get('company_name')
#             account.company_name = company_name
#             account.save()
#     return redirect('login')  # Redirect to the desired page after submission
import pdb
import random

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserCreationForm, CustomLoginForm, UpdateEmailForm, UserInfoForm, \
    VerificationForm, UpdatePasswordForm  # , ResendActivationEmailForm
from .models import Profile, CustomUser
from Account_Management.models import Account, AccountUserRelation
from django.contrib.auth.models import Group


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'User_Management/login.html'
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
            uid = force_str(urlsafe_base64_decode(uidb64))
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
                update_password_form.add_error('old_password', 'Old password is incorrect.')
            else:
                new_password1 = update_password_form.cleaned_data['new_password1']
                new_password2 = update_password_form.cleaned_data['new_password2']
                if new_password1 == new_password2:
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
                    messages.success(request, 'Password updated successfully.', extra_tags='signup')

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
                current_user.email = new_email
                current_user.save()
                messages.success(self.request, 'Email address updated successfully.', extra_tags='login')
                return redirect('user_setting')
            else:
                messages.error(self.request, 'Invalid verification code. Please try again.')

        return self.form_invalid(verify_form)


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

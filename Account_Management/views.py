from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from .models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        # Changes: consider 1-to-many auth user and user group
        account_activation_token = PasswordResetTokenGenerator()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            # try:
            #     user_group = AuthUserGroup.objects.filter(user_id=uid)
            # except ObjectDoesNotExist:
            #     return render(request, 'Account_Management/activation_failure.html')
            # for current_user_group in user_group:
            #     current_user_group.is_email_confirmed = True
            #     current_user_group.save()
            # first_group = user_group.order_by('-created_at').first()
            # user_account = Account.objects.get(pk=first_group.account_id.id)
            user.email_confirmed = True
            user.save()
            login(request, user)
            return render(request, 'Account_Management/activation_success.html')
        else:
            return render(request, 'Account_Management/activation_failure.html')
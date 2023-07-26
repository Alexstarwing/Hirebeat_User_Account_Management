from django.shortcuts import render
from django.views.generic.list import ListView
from Account_Management.models import Account
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


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


class AddUserView(LoginRequiredMixin, ListView):
    model = Account
    context_object_name = 'add_user'
    template_name = 'Account_Management/add_user.html'

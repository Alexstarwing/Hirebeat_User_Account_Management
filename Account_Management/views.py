'''
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
'''
from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
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
from .forms import UserCreationForm
from .models import Task
from .tokens import account_activation_token


class CustomLoginView(LoginView):
    template_name = 'Account_Management/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'Account_Management/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') #where user will be redirect after success registration bug
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account'
        message = render_to_string('Account_Management/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        send_mail(mail_subject, message, 'yifandsb666@gmail.com', [user.email])
        email_sent_message = "Activation email has been sent to your email address." #flash message
        messages.success(self.request, email_sent_message)
        return super().form_valid(form) #Redirect to success_url
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks') #Redirect to the home page
        return super().get(*args, **kwargs)

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token): #why always goes to else branch
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('tasks')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')
    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'Account_Management/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

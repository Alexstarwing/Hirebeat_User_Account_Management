from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileList, CustomLoginView, RegisterPage, ActivateAccount
from django.contrib.auth.views import LogoutView

# app_name = 'user_management'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', ProfileList.as_view(), name='profiles'),
    #     path('resend_activation_email/', resend_activation_email, name='resend_activation_email'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='User_Management/password_reset.html'),
         name='password_reset'),  # submit email form
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='User_Management/password_reset_sent.html'),
         name='password_reset_done'),  # Email sent success message
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='User_Management/password_reset_form.html'),
         name='password_reset_confirm'),  # Link to password reset form in email
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='User_Management/password_reset_done.html'),
         name='password_reset_complete'),  # Password successfully changed message
    
]

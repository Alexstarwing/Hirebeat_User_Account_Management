from django.urls import path
from .views import AccountList, AccountSettingView, ConfigureView, \
   AddUserView, OrganizationView, InvitationView, ManageUserView, RegisterWithInvitationView
from . import views
   

app_name = 'account_management'

urlpatterns = [
   path('', AccountList.as_view(), name='account'),
   path('edit_account/', AccountSettingView.as_view(), name='edit_account'),
   path('account_list/', ConfigureView.as_view(), name='account_list'),
   path('add_user/', AddUserView.as_view(), name='add_user'),
   path('invitation/', InvitationView.as_view(), name='invitation'),
   path('organization/', OrganizationView.as_view(), name='organization'),
   path('manage_users/', ManageUserView.as_view(), name='manage_users'),
   path('register/<invitation_token>/', RegisterWithInvitationView.as_view(), name='register_with_invitation'),
   path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
   path('create_or_update_employer/', views.create_or_update_employer_basic_info, name='create_or_update_employer'),
   
]
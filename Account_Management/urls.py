from django.urls import path
from .views import AccountList, EditAccountView, SettingView, \
   AddUserView, OrganizationView, InvitationView, ManageUserView
from . import views
   

app_name = 'account_management'

urlpatterns = [
   path('', AccountList.as_view(), name='account'),
   path('edit_account/', EditAccountView.as_view(), name='edit_account'),
   path('account_list/', SettingView.as_view(), name='account_list'),
   path('add_user/', AddUserView.as_view(), name='add_user'),
   path('invitation/', InvitationView.as_view(), name='invitation'),
   path('organization/', OrganizationView.as_view(), name='organization'),
   path('manage_users/', ManageUserView.as_view(), name='manage_users'),
]
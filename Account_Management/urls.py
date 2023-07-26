from django.urls import path
from .views import AccountList, EditAccountView, SettingView, AddUserView

app_name = 'account_management'

urlpatterns = [
   path('', AccountList.as_view(), name='account'),
   path('edit_account/', EditAccountView.as_view(), name='edit_account'),
   path('settings/', SettingView.as_view(), name='settings'),
   path('add_user/', AddUserView.as_view(), name='add_user'),
]

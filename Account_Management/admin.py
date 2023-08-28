from django.contrib import admin
from .models import Account, Role, TeamInvitation, AccountUserRelation

# Register your models here.
admin.site.register(Account)
admin.site.register(Role)
admin.site.register(TeamInvitation)
admin.site.register(AccountUserRelation)

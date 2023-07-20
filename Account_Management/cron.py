# from django.utils import timezone
# from django.contrib.auth import get_user_model

# #Crontab to set up a scheduled job (sets the time interval in setting.py)
# #Github explanation of Crontab: https://github.com/kraiz/django-crontab
# def delete_inactive_users():
#     User = get_user_model()

#     inactive_users = User.objects.filter(
#         date_joined__lt=timezone.now() - timezone.timedelta(seconds=1800), 
#         is_active=False,
#     ) #If not active after 30 mins, delete

#     inactive_users.delete()
# Generated by Django 3.2.8 on 2023-08-28 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Management', '0012_customuser_user_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_video',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2.8 on 2023-08-27 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Management', '0011_auto_20230815_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_logo',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]

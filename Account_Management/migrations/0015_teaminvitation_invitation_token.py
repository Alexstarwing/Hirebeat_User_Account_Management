# Generated by Django 3.2.8 on 2023-08-07 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Management', '0014_auto_20230807_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvitation',
            name='invitation_token',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True),
        ),
    ]

# Generated by Django 3.2.8 on 2023-08-02 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Management', '0002_account_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

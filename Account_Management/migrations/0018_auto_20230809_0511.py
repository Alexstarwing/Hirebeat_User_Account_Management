# Generated by Django 3.0 on 2023-08-09 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Management', '0017_auto_20230809_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='accountuserrelation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teaminvitation',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

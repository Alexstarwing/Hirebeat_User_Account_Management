# Generated by Django 3.2.8 on 2023-08-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Management', '0011_auto_20230815_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]

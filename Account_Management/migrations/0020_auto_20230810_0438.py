# Generated by Django 3.0 on 2023-08-10 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Management', '0019_teaminvitation_role'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['role'], name='Account_Man_role_id_a01a43_idx'),
        ),
    ]
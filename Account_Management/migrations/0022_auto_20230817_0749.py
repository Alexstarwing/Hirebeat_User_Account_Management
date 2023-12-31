# Generated by Django 3.2.8 on 2023-08-17 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_Management', '0021_auto_20230815_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='company_size_range',
            field=models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-200', '51-200'), ('201-500', '201-500'), ('501-1000', '501-1000'), ('1001+', '1001+')], max_length=255, null=True),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['company_industry'], name='Account_Man_company_89fe53_idx'),
        ),
    ]

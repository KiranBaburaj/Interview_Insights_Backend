# Generated by Django 5.0.6 on 2024-07-26 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='company_details_submitted',
            field=models.BooleanField(default=False),
        ),
    ]

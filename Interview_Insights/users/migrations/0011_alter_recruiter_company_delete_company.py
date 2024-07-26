# Generated by Django 5.0.6 on 2024-07-24 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_remove_companylocation_location'),
        ('users', '0010_remove_company_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.company'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]

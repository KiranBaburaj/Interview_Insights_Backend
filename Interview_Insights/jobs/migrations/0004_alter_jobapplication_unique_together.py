# Generated by Django 5.0.6 on 2024-07-28 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_applicationstage_jobapplication'),
        ('users', '0002_employer_company_details_submitted'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobapplication',
            unique_together={('job', 'job_seeker')},
        ),
    ]

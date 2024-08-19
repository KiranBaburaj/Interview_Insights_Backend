# Generated by Django 5.0.6 on 2024-08-18 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_job_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employment_type',
            field=models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'), ('Temporary', 'Temporary'), ('Internship', 'Internship'), ('Freelance', 'Freelance')], max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='experience_level',
            field=models.CharField(blank=True, choices=[('Entry level', 'Entry level'), ('Mid level', 'Mid level'), ('Senior level', 'Senior level'), ('Executive', 'Executive')], max_length=50, null=True),
        ),
    ]

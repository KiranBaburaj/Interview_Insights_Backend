# Generated by Django 4.2.7 on 2024-07-14 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0001_initial'),
        ('users', '0002_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='company_name',
        ),
        migrations.AddField(
            model_name='employer',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employer.company'),
        ),
    ]

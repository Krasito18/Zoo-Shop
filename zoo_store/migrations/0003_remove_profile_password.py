# Generated by Django 5.1.6 on 2025-04-07 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_store', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
    ]

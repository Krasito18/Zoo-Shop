# Generated by Django 5.0.4 on 2025-03-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo_store', '0003_checkoutinfo_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutinfo',
            name='country_reference',
        ),
        migrations.AddField(
            model_name='checkoutinfo',
            name='country',
            field=models.CharField(choices=[('US', 'United States'), ('CA', 'Canada'), ('UK', 'United Kingdom'), ('AU', 'Australia')], default='USD', max_length=30),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Country',
        ),
    ]

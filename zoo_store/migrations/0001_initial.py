# Generated by Django 5.0.4 on 2025-03-21 13:33

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('currency', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=15)),
                ('street_address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=30)),
                ('name_on_card', models.CharField(max_length=100)),
                ('payment_token', models.CharField(max_length=255)),
                ('expiration_date', models.CharField(max_length=6)),
                ('cvv', models.CharField(max_length=5)),
                ('country_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to='zoo_store.country')),
            ],
        ),
    ]

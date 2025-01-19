# Generated by Django 5.1.3 on 2025-01-19 18:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Shipping_full_name', models.CharField(max_length=100)),
                ('Shipping_email', models.EmailField(blank=True, max_length=100)),
                ('Shipping_phone_number', models.CharField(blank=True, max_length=15)),
                ('Shipping_province', models.CharField(blank=True, max_length=25)),
                ('Shipping_city', models.CharField(blank=True, max_length=25)),
                ('Shipping_address1', models.CharField(blank=True, max_length=100)),
                ('Shipping_postal_code', models.CharField(blank=True, max_length=10)),
                ('Shipping_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

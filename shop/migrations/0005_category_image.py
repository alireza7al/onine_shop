# Generated by Django 5.1.3 on 2024-12-14 13:45

import shop.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_customer_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.category_image_upload_to),
        ),
    ]
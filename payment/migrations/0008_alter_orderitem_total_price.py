# Generated by Django 5.1.3 on 2025-01-21 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_orderitem_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='total_price',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

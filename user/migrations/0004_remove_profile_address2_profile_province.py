# Generated by Django 5.1.3 on 2025-01-19 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile_old_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address2',
        ),
        migrations.AddField(
            model_name='profile',
            name='province',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]

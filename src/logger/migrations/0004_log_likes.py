# Generated by Django 4.2.3 on 2023-07-14 06:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logger', '0003_rename_profile_photo_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='log_like', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-16 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0005_alter_log_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='replay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='logger.log'),
        ),
    ]

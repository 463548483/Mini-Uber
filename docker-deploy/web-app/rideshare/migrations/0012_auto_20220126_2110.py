# Generated by Django 2.2.12 on 2022-01-26 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rideshare', '0011_driver_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='username',
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

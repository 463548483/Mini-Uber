# Generated by Django 4.0.1 on 2022-01-30 20:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0015_alter_rides_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rides',
            name='has_sharer',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N')], default='N', max_length=5, verbose_name='Has Sharer'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='capacity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Passenger Capacity'),
        ),
        migrations.AlterField(
            model_name='rides',
            name='number_passenger',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Passenger Number'),
        ),
        migrations.AlterField(
            model_name='sharer_search',
            name='number_passenger',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Passenger Number'),
        ),
    ]

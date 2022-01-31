# Generated by Django 4.0.1 on 2022-01-25 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0005_remove_driver_username_alter_rides_number_passenger_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rides',
            name='share',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, verbose_name='Share Ride'),
        ),
        migrations.AlterField(
            model_name='rides',
            name='special_request',
            field=models.TextField(blank=True, verbose_name='Special Request'),
        ),
        migrations.AlterField(
            model_name='rides',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=20, verbose_name='Vehicle Requirement'),
        ),
    ]

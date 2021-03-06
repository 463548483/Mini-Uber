# Generated by Django 4.0.1 on 2022-01-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Driver Name')),
                ('vehicle_type', models.CharField(max_length=30, verbose_name='Vehicle Type')),
                ('license_number', models.CharField(max_length=30, verbose_name='License Plate Number')),
                ('capacity', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Passenger Capacity')),
                ('special_vehicle_info', models.TextField(verbose_name='Special Vehicle Information')),
            ],
        ),
        migrations.CreateModel(
            name='Rides',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Request_id')),
                ('destination', models.CharField(max_length=100, verbose_name='Destination')),
                ('arrive_date', models.DateTimeField(auto_now_add=True, verbose_name='Request Arrival Date and Time')),
                ('number_passenger', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Passenger Number')),
                ('share', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Share Ride')),
                ('status', models.DecimalField(choices=[(1, 'Open'), (2, 'Confirmed'), (3, 'Closed')], decimal_places=0, default=1, max_digits=3, verbose_name='Status')),
                ('vehicle_type', models.CharField(max_length=20, verbose_name='Vehicle Requirement')),
                ('special_request', models.TextField(verbose_name='Special Request')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=24, verbose_name='Account')),
                ('password', models.CharField(max_length=24, verbose_name='Password')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
        ),
    ]

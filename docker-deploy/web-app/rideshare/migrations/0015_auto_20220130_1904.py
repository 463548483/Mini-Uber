# Generated by Django 2.2.12 on 2022-01-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0014_alter_driver_id_alter_sharer_search_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='sharer_search',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

# Generated by Django 2.2.12 on 2022-01-26 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshare', '0009_sharer_search_join_ride'),
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

# Generated by Django 3.2.2 on 2021-05-25 11:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='block_a',
        ),
        migrations.RemoveField(
            model_name='block',
            name='block_b',
        ),
        migrations.RemoveField(
            model_name='block',
            name='block_c',
        ),
        migrations.RemoveField(
            model_name='block',
            name='block_d',
        ),
        migrations.AddField(
            model_name='block',
            name='block',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, size=None),
        ),
    ]
# Generated by Django 3.2.2 on 2021-05-25 11:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS_app', '0002_auto_20210525_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='block',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=[], size=None),
        ),
    ]

# Generated by Django 3.2.2 on 2021-05-26 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CMS_app', '0005_collection_cam_received_collection_dg_collection_electricity_collection_rent_collection_water_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection_dg',
            old_name='bil_received',
            new_name='bill_received',
        ),
    ]

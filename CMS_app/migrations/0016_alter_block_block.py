# Generated by Django 3.2.2 on 2021-06-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS_app', '0015_merge_0013_auto_20210601_2102_0014_alter_block_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='block',
            field=models.CharField(max_length=100),
        ),
    ]
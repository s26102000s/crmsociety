# Generated by Django 3.2.2 on 2021-06-02 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS_app', '0016_alter_block_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_for',
            field=models.CharField(choices=[('Water', 'Water'), ('Electricity', 'Electricity')], max_length=100),
        ),
    ]

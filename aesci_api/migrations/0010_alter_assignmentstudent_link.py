# Generated by Django 3.2.5 on 2021-10-12 04:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0009_alter_assignmentstudent_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentstudent',
            name='link',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=8),
        ),
    ]

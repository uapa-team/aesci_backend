# Generated by Django 3.2.8 on 2022-01-30 02:44

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0005_alter_assignment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='link',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=2),
        ),
    ]
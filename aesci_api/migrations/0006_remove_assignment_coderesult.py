# Generated by Django 3.2.5 on 2021-09-07 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0005_indicatorassignment_indicatorgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='codeResult',
        ),
    ]

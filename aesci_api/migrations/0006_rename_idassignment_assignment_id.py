# Generated by Django 3.2.8 on 2022-01-20 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0005_alter_indicatorassignment_assignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='idAssignment',
            new_name='id',
        ),
    ]
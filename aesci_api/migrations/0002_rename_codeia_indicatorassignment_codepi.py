# Generated by Django 3.2.5 on 2021-09-01 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indicatorassignment',
            old_name='codeIA',
            new_name='codePI',
        ),
    ]
# Generated by Django 3.2.8 on 2022-01-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0002_rename_username_assignment_usernameteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='link',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]

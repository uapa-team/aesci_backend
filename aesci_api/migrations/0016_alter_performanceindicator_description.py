# Generated by Django 3.2.8 on 2021-11-02 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0015_alter_studentoutcome_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceindicator',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]

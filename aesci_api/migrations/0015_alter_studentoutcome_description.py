# Generated by Django 3.2.8 on 2021-11-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0014_alter_evaluationassignment_documentattached'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentoutcome',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]